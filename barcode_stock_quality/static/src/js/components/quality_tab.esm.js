import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {user} from "@web/core/user";

/**
 * Quality tab of a reception: lists the quality inspections that the reception
 * generated (via quality_control_stock_oca), lets the operator answer each one
 * and, when a check does not pass, attach a photo as evidence.
 *
 * Inspections are Quality Control users' business, as in the back office: any
 * other operator is told so in the tab.
 *
 * The answers not confirmed yet are kept by the reception screen (`answers`),
 * which lives on while the operator looks at another tab: leaving the Quality
 * tab, which unmounts it, loses none of them.
 */
export class QualityTab extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.answers = useState(this.props.answers || {});
        this.state = useState({
            inspections: [],
            loading: true,
            busyId: null,
            canInspect: true,
        });

        onWillStart(() => this.loadTab());
    }

    async loadTab() {
        this.state.canInspect = await user.hasGroup(
            "quality_control_oca.group_quality_control_user"
        );
        if (this.state.canInspect) {
            await this.loadInspections();
        } else {
            this.state.loading = false;
        }
    }

    async loadInspections() {
        this.state.loading = true;
        try {
            const result = await this.inventory.call(
                "stock.picking",
                "action_barcode_scanner_quality_inspections",
                [this.props.pickingId]
            );
            this.state.inspections = result.inspections;
        } catch {
            // The API wrapper already told the operator what went wrong.
        } finally {
            this.state.loading = false;
        }
    }

    answersFor(inspection) {
        if (!this.answers[inspection.inspection_id]) {
            this.answers[inspection.inspection_id] = {};
        }
        return this.answers[inspection.inspection_id];
    }

    setQualitative(inspection, line, valueId) {
        this.answersFor(inspection)[line.id] = {
            line_id: line.id,
            qualitative_value_id: valueId,
        };
    }

    onQuantitative(inspection, line, ev) {
        // A measure left blank is no answer, not a 0 to be judged.
        const text = ev.target.value.trim();
        const value = Number(text);
        const answers = this.answersFor(inspection);
        if (text === "" || !Number.isFinite(value)) {
            delete answers[line.id];
            return;
        }
        answers[line.id] = {line_id: line.id, quantitative_value: value};
    }

    /**
     * The measure an input shows: the one typed, or none.
     *
     * @param {Object} inspection the inspection
     * @param {Object} line its quantitative question
     * @returns {Number|String} the measure, or an empty string
     */
    measureOf(inspection, line) {
        return this.answersFor(inspection)[line.id]?.quantitative_value ?? "";
    }

    isChosen(inspection, line, valueId) {
        return this.answersFor(inspection)[line.id]?.qualitative_value_id === valueId;
    }

    // Only a ready inspection is answered; a confirmed one is shown read-only
    // and reopened with "Back to draft" to correct it.
    isEditable(inspection) {
        return inspection.state === "ready";
    }

    answerLabel(line) {
        if (line.question_type === "qualitative") {
            return line.qualitative_value_name;
        }
        return line.uom_name
            ? `${line.quantitative_value} ${line.uom_name}`
            : String(line.quantitative_value);
    }

    allAnswered(inspection) {
        return inspection.lines.every((line) => {
            const answer = this.answersFor(inspection)[line.id];
            if (line.question_type === "qualitative") {
                return Boolean(answer?.qualitative_value_id);
            }
            return Number.isFinite(answer?.quantitative_value);
        });
    }

    async submit(inspection) {
        if (this.state.busyId || !this.allAnswered(inspection)) {
            return;
        }
        this.state.busyId = inspection.inspection_id;
        try {
            const answers = Object.values(this.answersFor(inspection));
            const updated = await this.inventory.call(
                "qc.inspection",
                "action_barcode_scanner_submit",
                [inspection.inspection_id, answers]
            );
            delete this.answers[inspection.inspection_id];
            this.replaceInspection(updated);
            this.inventory.notify(
                updated.success
                    ? _t("Inspection %(name)s passed.", {name: updated.inspection_name})
                    : _t("Inspection %(name)s failed.", {
                          name: updated.inspection_name,
                      }),
                {type: updated.success ? "success" : "warning"}
            );
        } catch {
            // The API wrapper already told the operator what went wrong.
        } finally {
            this.state.busyId = null;
        }
    }

    isConfirmed(inspection) {
        return ["success", "waiting", "failed"].includes(inspection.state);
    }

    // The server says which ones the scanner may reopen: those it confirmed,
    // no supervisor has decided and whose reception is still open.
    canReset(inspection) {
        return Boolean(inspection.can_reset);
    }

    /**
     * Fill the answers in from an inspection's questions: back to draft keeps
     * them, for the operator to correct what was wrong.
     *
     * @param {Object} inspection the inspection as the server returned it
     */
    seedAnswers(inspection) {
        const answers = {};
        for (const line of inspection.lines) {
            if (line.question_type === "qualitative") {
                if (line.qualitative_value_id) {
                    answers[line.id] = {
                        line_id: line.id,
                        qualitative_value_id: line.qualitative_value_id,
                    };
                }
            } else {
                answers[line.id] = {
                    line_id: line.id,
                    quantitative_value: line.quantitative_value,
                };
            }
        }
        this.answers[inspection.inspection_id] = answers;
    }

    async reset(inspection) {
        if (this.state.busyId) {
            return;
        }
        this.state.busyId = inspection.inspection_id;
        try {
            const updated = await this.inventory.call(
                "qc.inspection",
                "action_barcode_scanner_reset",
                [inspection.inspection_id]
            );
            this.seedAnswers(updated);
            this.replaceInspection(updated);
            this.inventory.notify(
                _t("Inspection %(name)s is back to draft.", {
                    name: updated.inspection_name,
                }),
                {type: "info"}
            );
        } catch {
            // The API wrapper already told the operator what went wrong.
        } finally {
            this.state.busyId = null;
        }
    }

    async onPhotoSelected(inspection, ev) {
        const file = ev.target.files && ev.target.files[0];
        ev.target.value = "";
        if (!file || this.state.busyId) {
            return;
        }
        this.state.busyId = inspection.inspection_id;
        try {
            let photo = null;
            try {
                photo = await this.readPhoto(file);
            } catch {
                this.inventory.notify(_t("The photo could not be read."), {
                    type: "danger",
                });
                return;
            }
            const result = await this.inventory.call(
                "qc.inspection",
                "action_barcode_scanner_attach_photo",
                [inspection.inspection_id, photo.name, photo.datas]
            );
            inspection.photo_count = result.photo_count;
            this.inventory.notify(_t("Photo attached."), {type: "success"});
        } catch {
            // The API wrapper already told the operator what went wrong.
        } finally {
            this.state.busyId = null;
        }
    }

    // Read the chosen photo, shrinking it to a reasonable evidence size. Phone
    // cameras produce multi-megapixel images whose upload a reverse proxy may
    // reject as too large, so the picture is scaled down (longest side capped)
    // and re-encoded as JPEG. Non-images, or a browser without canvas support,
    // keep the untouched file.
    async readPhoto(file, maxSide = 1600, quality = 0.82) {
        if (file.type && file.type.startsWith("image/")) {
            try {
                const bitmap = await createImageBitmap(file, {
                    imageOrientation: "from-image",
                });
                const scale = Math.min(
                    1,
                    maxSide / Math.max(bitmap.width, bitmap.height)
                );
                const canvas = document.createElement("canvas");
                canvas.width = Math.max(1, Math.round(bitmap.width * scale));
                canvas.height = Math.max(1, Math.round(bitmap.height * scale));
                const context = canvas.getContext("2d");
                if (context) {
                    context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
                    bitmap.close();
                    const datas = canvas.toDataURL("image/jpeg", quality).split(",")[1];
                    if (datas) {
                        const name = file.name.replace(/\.[^./\\]+$/, "") + ".jpg";
                        return {name, datas};
                    }
                } else {
                    bitmap.close();
                }
            } catch {
                // A browser without createImageBitmap/canvas keeps the raw file.
            }
        }
        return {name: file.name, datas: await this.readAsBase64(file)};
    }

    readAsBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(",")[1] || "");
            reader.onerror = () => reject(reader.error);
            reader.readAsDataURL(file);
        });
    }

    replaceInspection(updated) {
        const index = this.state.inspections.findIndex(
            (i) => i.inspection_id === updated.inspection_id
        );
        if (index !== -1) {
            this.state.inspections[index] = {
                ...updated,
                photo_count: this.state.inspections[index].photo_count,
            };
        }
    }
}

QualityTab.template = "barcode_stock_quality.QualityTab";
QualityTab.props = {
    pickingId: {type: [Number, {value: false}]},
    answers: {type: Object, optional: true},
};
