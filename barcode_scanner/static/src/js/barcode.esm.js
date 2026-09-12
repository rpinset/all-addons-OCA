import {EventBus} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {session} from "@web/session";
import {parseBarcode} from "@barcode_scanner/js/barcode_parser.esm";

/**
 * Barcode capture for the scanning SPA, built for the Munbyn Android PDAs used
 * by Donaldson and Spartan.
 *
 * These PDAs deliver every laser scan through the Android input method (IME),
 * not as real key events: each keystroke arrives as `keydown key="Unidentified"`
 * (keyCode 0/229) and the actual code is committed as TEXT into the focused
 * field's `.value`. So we keep a hidden, focused <input> and read the scan from
 * its `.value` on the terminating Enter/Tab (or shortly after the bulk `input`
 * event for scanners that send no Enter).
 *
 * The input must STAY a plain editable field: anything that hides the Android
 * soft keyboard for good -- `inputmode="none"` OR the VirtualKeyboard API --
 * also closes the IME composition session on this hardware, after which the
 * scanner reads only once per Chrome session (proven on-device, see the
 * barcode-pda-scanner-ime-only note). To keep the laser reading on every screen
 * without the soft keyboard popping up, we focus() the field while it is
 * briefly `readonly` and restore it to editable right after: a readonly field
 * never raises the soft keyboard on Android Chrome, yet it stays focused and
 * connected to the IME the whole time. Flip HIDE_SOFT_KEYBOARD below to false
 * if a PDA stops reading after the first scan (its IME only injects while the
 * keyboard is actually up).
 *
 * A permanent on-screen "scan feedback" toast shows the full code the PDA just
 * read, then fades, so a misread or a dead scan is visible instead of silent.
 */

// GS1 FNC1 group separator (the real control char the parser splits on).
const GS1_FNC1 = String.fromCharCode(29);

// Scanners / the Android IME sometimes deliver the FNC1 separator not as the
// real 0x1D control char but as its visible Unicode symbol (U+241D), a nearby
// separator symbol, or a replacement box (U+FFFD). Normalise all back to 0x1D so
// the GS1 parser detects the barcode as GS1 and splits the AIs.
const GS1_SEPARATOR_VARIANTS = /[␝␞␟�]/g;
function normalizeGs1Separators(str) {
    return str.replace(GS1_SEPARATOR_VARIANTS, GS1_FNC1);
}

// For the on-screen feedback: render control chars (incl. the GS1 separator),
// the "control pictures" block and the replacement box as a visible middot, so
// the whole scanned code stays readable.
const NON_PRINTABLE = /[\x00-\x1f\x7f␀-␿�]/g;

function isEditable(element) {
    if (!element || element.nodeType !== 1) {
        return false;
    }
    return (
        element.matches('input, textarea, select, [contenteditable="true"]') ||
        element.isContentEditable
    );
}

// Real interactive targets the user is deliberately operating: we must not steal
// focus from these, so their own keyboard shows and they can type -- and native
// pop-ups (a <select> dropdown, a date picker) can open. Such a control steals
// focus the instant it is clicked, which our keep-focus guard would otherwise
// yank straight back, closing it before it opens (the desktop "the lot picker /
// date field trembles but won't open" bug); matching them here leaves them
// alone. The hidden barcode-capture input is a text input too, so exclude it
// explicitly -- focus must always return to it.
function isUserEditable(element) {
    if (!element || element.nodeType !== 1) {
        return false;
    }
    if (element.classList && element.classList.contains("o-barcode-input")) {
        return false;
    }
    return element.matches("input, textarea, select, [contenteditable]");
}

// Keep the Android soft keyboard closed. Our hidden input is focused() while
// momentarily `readonly`, which Chrome never honours by raising the keyboard,
// then restored to editable, so the scanner IME session stays alive on the
// focused field. If a PDA stops reading after the first scan because its IME
// only injects while the keyboard is actually visible, flip this to false.
const HIDE_SOFT_KEYBOARD = true;

export const barcodeService = {
    dependencies: [],
    maxTimeBetweenKeysInMs: session.max_time_between_keys_in_ms || 150,

    start() {
        const bus = new EventBus();
        let timeout = null;
        let readonlyTimer = null;
        let barcodeInput = null;
        let fbEl = null;
        let fbTimer = null;
        let active = false;
        // Desktop keyboard-wedge (USB scanner / Chrome barcode extension) buffer.
        // Real keystrokes accumulate here; the PDA laser never uses it -- its keys
        // arrive as "Unidentified" IME text, flushed via the input event instead.
        let keyBuffer = "";
        let keyBufferTimer = null;

        // Focus the hidden capture input WITHOUT raising the Android soft
        // keyboard: Chrome never shows the keyboard for a focus() on a readonly
        // field, but the field stays focused and connected to the IME, so the
        // scanner keeps injecting. We restore it to a normal editable field just
        // after the focus has settled (still no user gesture, so no keyboard
        // pop), which is what keeps the IME composition session alive -- the
        // very thing `inputmode="none"` would have closed.
        function focusCaptureInput() {
            if (!barcodeInput) {
                return;
            }
            if (!HIDE_SOFT_KEYBOARD) {
                try {
                    barcodeInput.focus({preventScroll: true});
                } catch {
                    barcodeInput.focus();
                }
                return;
            }
            const input = barcodeInput;
            input.readOnly = true;
            try {
                input.focus({preventScroll: true});
            } catch {
                input.focus();
            }
            clearTimeout(readonlyTimer);
            readonlyTimer = setTimeout(() => {
                input.readOnly = false;
            }, 50);
        }

        // --- Permanent scan feedback: a centred toast showing the full code the
        // PDA just read, then fading out, so a misread or dead scan is obvious. ---
        function makeFeedbackEl() {
            const el = document.createElement("div");
            el.setAttribute(
                "style",
                "position:fixed;top:10px;left:50%;transform:translateX(-50%);" +
                    "z-index:2147483646;max-width:92vw;box-sizing:border-box;" +
                    "padding:8px 14px;border-radius:9px;background:rgba(20,20,20,.92);" +
                    "color:#fff;font:600 13px/1.3 monospace;white-space:normal;" +
                    "word-break:break-all;pointer-events:none;" +
                    "opacity:0;transition:opacity .2s ease;" +
                    "box-shadow:0 2px 10px rgba(0,0,0,.45);"
            );
            return el;
        }

        function showScanFeedback(received) {
            if (!fbEl) {
                return;
            }
            fbEl.textContent = String(received || "").replace(NON_PRINTABLE, "·");
            fbEl.style.opacity = "1";
            clearTimeout(fbTimer);
            fbTimer = setTimeout(() => {
                if (fbEl) {
                    fbEl.style.opacity = "0";
                }
            }, 2500);
        }
        // --- end scan feedback ---

        function emit(raw) {
            const received = String(raw || "")
                .replace(/Alt|Shift|Control/g, "")
                .replace(/[\r\n]+$/, "");
            const code = normalizeGs1Separators(received);
            const significant = code.replace(/[\r\n]/g, "");
            if (significant.length >= 3) {
                bus.trigger("barcode_scanned", {
                    barcode: code,
                    parsed: parseBarcode(code),
                });
            }
            // Always show what the PDA just read (permanent feedback), even when
            // it is too short/garbled to emit, so the operator/support can tell a
            // "read nothing" apart from a "read the wrong thing".
            showScanFeedback(received);
        }

        // Read the scan from the hidden input's value and emit it. The PDA laser
        // arrives via the Android IME, which commits the whole code into the
        // input's `.value`; we flush it on the terminating Enter/Tab (onKeyDown)
        // or shortly after the bulk `input` event (onImeInput).
        function checkBarcode(ev) {
            const str = barcodeInput ? barcodeInput.value : "";
            if (str && str.replace(/[\r\n]/g, "").length >= 3) {
                if (ev) {
                    ev.preventDefault();
                }
                emit(str);
            }
            clearTimeout(timeout);
            timeout = null;
            if (barcodeInput) {
                barcodeInput.value = "";
            }
        }

        // Emit a desktop keyboard-wedge scan gathered in keyBuffer, and clear the
        // capture input too so the same code is never also emitted by checkBarcode
        // from the input value.
        function flushKeyBuffer(ev) {
            const buf = keyBuffer;
            keyBuffer = "";
            clearTimeout(keyBufferTimer);
            keyBufferTimer = null;
            if (barcodeInput) {
                barcodeInput.value = "";
            }
            if (buf.replace(/[\r\n]/g, "").length >= 3) {
                if (ev) {
                    ev.preventDefault();
                }
                emit(buf);
            }
        }

        function onKeyDown(ev) {
            if (!ev.key || ev.key === "Unidentified") {
                // IME character noise: the real text is in barcodeInput.value.
                // Do NOT touch focus here -- refocusing mid-composition kills the
                // IME session on this hardware.
                return;
            }

            // On a REAL key, if focus is not on a user-editable field, pull it
            // back to our hidden input so the terminating Enter (and the value it
            // flushes) is ours. This runs only on real keys, never on the
            // Unidentified IME stream above (mirrors Odoo core's mobile handler).
            if (
                barcodeInput &&
                document.activeElement &&
                document.activeElement !== barcodeInput &&
                !isUserEditable(document.activeElement)
            ) {
                focusCaptureInput();
            }

            const isSpecialKey =
                !["Control", "Alt"].includes(ev.key) &&
                (ev.key.length > 1 || ev.metaKey);
            const isEndCharacter = /(Enter|Tab)/.test(ev.key);

            // Don't capture while the user is deliberately typing into a real
            // field (search boxes, quantity/lot inputs).
            const target = ev.target;
            const typingInUserField =
                target !== barcodeInput &&
                isEditable(target) &&
                !(target.dataset && target.dataset.enableBarcode);

            // Desktop keyboard-wedge: a real printable key never comes from the
            // PDA laser (that arrives as "Unidentified" above), so gather real
            // keys into keyBuffer and flush on Enter/Tab or a short pause. We read
            // ev.key directly, so it works even while the capture input is briefly
            // readonly for the soft-keyboard trick and the chars never reach its
            // value. The PDA keeps its own path: keyBuffer stays empty there, so
            // its terminating Enter still falls through to checkBarcode below.
            if (!typingInUserField && !isSpecialKey && !isEndCharacter) {
                // Mirror Odoo core: capture ctrl/alt-modified keys too, because a
                // GS1 label carries its group separator (FNC1) that way. A raw
                // 0x1D arrives as its own single char; the common Ctrl+] form is
                // mapped to the real FNC1 so variable-length AIs (lot/serial) stay
                // delimited and the lot parses on desktop as it does on the PDA.
                // Stray modifier-key names (Control/Alt/Shift) are stripped by
                // emit()'s cleanup.
                keyBuffer += ev.ctrlKey && ev.key === "]" ? GS1_FNC1 : ev.key;
                clearTimeout(keyBufferTimer);
                keyBufferTimer = setTimeout(
                    flushKeyBuffer,
                    barcodeService.maxTimeBetweenKeysInMs
                );
            }

            if (isSpecialKey && !isEndCharacter) {
                return;
            }
            if (typingInUserField) {
                return;
            }

            if (isEndCharacter) {
                // A desktop wedge scan ends here (flush the buffer); a PDA/IME scan
                // has its text in the input value (checkBarcode). keyBuffer is
                // always empty on the PDA, so it never changes that path.
                if (keyBuffer) {
                    flushKeyBuffer(ev);
                } else {
                    checkBarcode(ev);
                }
            }
        }

        // Bulk IME commit fires an `input` event: flush the value shortly after,
        // so scanners that send no Enter still work. An Enter, when it comes,
        // flushes instantly via onKeyDown.
        function onImeInput() {
            clearTimeout(timeout);
            timeout = setTimeout(checkBarcode, barcodeService.maxTimeBetweenKeysInMs);
        }

        // The IME only composes while our hidden input holds focus. After the app
        // mounts (and after a tap on a button) focus lands on <body>, so return
        // it to the input. A plain re-focus of the SAME element -- never a blur or
        // recreate, which close the IME session on this hardware.
        //
        // We always focus through focusCaptureInput() (readonly-focus trick), so
        // reclaiming focus never summons the Android soft keyboard.
        function keepFocus() {
            if (!active || !barcodeInput || !document.body.contains(barcodeInput)) {
                return;
            }
            if (document.querySelector(".o_dialog, .modal")) {
                return;
            }
            const el = document.activeElement;
            if (el === barcodeInput || isUserEditable(el)) {
                return;
            }
            focusCaptureInput();
        }

        function onFocusOut() {
            setTimeout(keepFocus, 0);
        }

        function makeBarcodeInput() {
            const el = document.createElement("input");
            el.setAttribute("type", "text");
            el.setAttribute("autocomplete", "off");
            // A NORMAL editable input is required for the PDA laser to read
            // reliably: `inputmode="none"` or the VirtualKeyboard API also close
            // the IME composition session (see the header note). The soft
            // keyboard itself is kept closed by the readonly focus() trick in
            // focusCaptureInput(), which never hides the field from the IME.
            el.classList.add("o-barcode-input");
            el.setAttribute("name", "barcode");
            el.setAttribute(
                "style",
                "position:fixed;top:50%;transform:translateY(-50%);z-index:-1;opacity:0"
            );
            return el;
        }

        function activate() {
            if (active) {
                return;
            }
            active = true;
            barcodeInput = makeBarcodeInput();
            document.body.appendChild(barcodeInput);
            barcodeInput.addEventListener("input", onImeInput);
            document.addEventListener("focusout", onFocusOut, true);
            fbEl = makeFeedbackEl();
            document.body.appendChild(fbEl);
            // Grab focus now and again once the screen has rendered (OWL mounts
            // the screen right after us and focus otherwise falls back to body).
            keepFocus();
            setTimeout(keepFocus, 300);
        }

        function deactivate() {
            if (!active) {
                return;
            }
            active = false;
            clearTimeout(timeout);
            timeout = null;
            clearTimeout(readonlyTimer);
            readonlyTimer = null;
            clearTimeout(keyBufferTimer);
            keyBufferTimer = null;
            keyBuffer = "";
            clearTimeout(fbTimer);
            fbTimer = null;
            document.removeEventListener("focusout", onFocusOut, true);
            if (barcodeInput) {
                barcodeInput.removeEventListener("input", onImeInput);
                barcodeInput.remove();
                barcodeInput = null;
            }
            if (fbEl) {
                fbEl.remove();
                fbEl = null;
            }
        }

        document.addEventListener("keydown", onKeyDown, true);

        return {
            bus,
            parseBarcode,
            activate,
            deactivate,
            destroy() {
                document.removeEventListener("keydown", onKeyDown, true);
                clearTimeout(timeout);
                deactivate();
            },
        };
    },
};
registry.category("services").add("barcodeScannerBarcode", barcodeService);
