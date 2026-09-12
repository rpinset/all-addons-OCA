import {Reactive} from "@web/core/utils/reactive";
import {registry} from "@web/core/registry";

const DEFAULT_PROFILES = {
    success: {
        vibration: [35],
        audio: {frequency: 880, duration: 0.08, type: "sine", volume: 0.03},
    },
    warning: {
        vibration: [20, 30, 20],
        audio: {frequency: 540, duration: 0.12, type: "triangle", volume: 0.03},
    },
    error: {
        vibration: [40, 20, 40],
        audio: {frequency: 220, duration: 0.18, type: "sawtooth", volume: 0.035},
    },
    info: {
        vibration: [],
        audio: {frequency: 660, duration: 0.06, type: "sine", volume: 0.02},
    },
};

function nextMicrotask(callback) {
    if (typeof queueMicrotask === "function") {
        queueMicrotask(callback);
    } else {
        Promise.resolve().then(callback);
    }
}

export class BarcodeScannerFeedbackService extends Reactive {
    constructor(notification) {
        super();
        this.setup(notification);
    }

    setup(notification) {
        this.notification = notification;
        this.enabled = {audio: true, vibration: true, flash: true};
        this.capabilities = {
            audio:
                typeof window !== "undefined" &&
                Boolean(window.AudioContext || window.webkitAudioContext),
            vibration:
                typeof navigator !== "undefined" &&
                typeof navigator.vibrate === "function",
            flash: true,
        };
        this.flash = {active: false, level: "info", token: 0};
        this.lastSignal = null;
        this._audioContext = null;
        this._flashTimeout = null;
    }

    destroy() {
        if (this._flashTimeout) {
            clearTimeout(this._flashTimeout);
            this._flashTimeout = null;
        }
        if (this._audioContext?.close) {
            this._audioContext.close();
        }
    }

    success(options = {}) {
        return this.signal("success", options);
    }

    warning(options = {}) {
        return this.signal("warning", options);
    }

    error(options = {}) {
        return this.signal("error", options);
    }

    info(options = {}) {
        return this.signal("info", options);
    }

    signal(level, options = {}) {
        const profile = DEFAULT_PROFILES[level] || DEFAULT_PROFILES.info;
        const signal = {level, message: options.message || "", at: Date.now()};
        this.lastSignal = signal;
        if (options.notify && options.message) {
            this.notification.add(options.message, {type: level});
        }
        if (this.enabled.flash) {
            this.flashOnce(level, options.flashDurationMs || 180);
        }
        if (this.enabled.vibration && profile.vibration.length) {
            this.vibrate(options.vibrationPattern || profile.vibration);
        }
        if (this.enabled.audio) {
            this.playTone(options.audio || profile.audio);
        }
        return signal;
    }

    flashOnce(level = "info", duration = 180) {
        if (this._flashTimeout) {
            clearTimeout(this._flashTimeout);
        }
        this.flash.active = false;
        this.flash.level = level;
        this.flash.token += 1;
        nextMicrotask(() => {
            this.flash.active = true;
            this._flashTimeout = setTimeout(() => {
                this.flash.active = false;
                this._flashTimeout = null;
            }, duration);
        });
    }

    vibrate(pattern) {
        if (!this.capabilities.vibration || !this.enabled.vibration) {
            return false;
        }
        return Boolean(navigator.vibrate(pattern));
    }

    playTone({frequency, duration, type, volume}) {
        if (!this.capabilities.audio || !this.enabled.audio) {
            return false;
        }
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            this._audioContext = this._audioContext || new AudioContextClass();
            const context = this._audioContext;
            const oscillator = context.createOscillator();
            const gain = context.createGain();
            oscillator.type = type;
            oscillator.frequency.value = frequency;
            gain.gain.value = volume;
            oscillator.connect(gain);
            gain.connect(context.destination);
            const now = context.currentTime;
            oscillator.start(now);
            oscillator.stop(now + duration);
            return true;
        } catch {
            return false;
        }
    }
}

export const barcodeScannerFeedbackService = {
    dependencies: ["notification"],
    start(env, {notification}) {
        return new BarcodeScannerFeedbackService(notification);
    },
};

registry
    .category("services")
    .add("barcodeScannerFeedback", barcodeScannerFeedbackService);
