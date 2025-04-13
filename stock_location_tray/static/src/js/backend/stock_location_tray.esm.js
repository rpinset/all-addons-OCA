// Copyright 2019 Camptocamp SA
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import {Component, onMounted, onWillDestroy, useEffect, useRef} from "@odoo/owl";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useService} from "@web/core/utils/hooks";

const {Object, Math} = globalThis;

export class LocationTrayMatrixField extends Component {
    /**
     * Shows a canvas with the Tray's cells
     *
     * An action can be configured which is called when a cell is clicked.
     * The action must be an action.multi, it will receive the x and y positions
     * of the cell clicked (starting from 0). The action must be configured in
     * the options of the field and be on the same model:
     *
     * <field name="tray_matrix"
     *        widget="location_tray_matrix"
     *        options="{'click_action': 'action_tray_matrix_click'}"
     *        />
     *
     **/
    static template = "stock_location_tray.LocationTrayMatrix";
    static props = {
        ...standardFieldProps,
        clickAction: {type: String, optional: true},
    };
    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
        this.canvasRef = useRef("canvas");
        this._ready = false;
        this._resizePromise = null;
        this.cellColorEmpty = "#ffffff";
        this.cellColorNotEmpty = "#4e6bfd";
        this.selectedColor = "#08f46b";
        this.selectedLineWidth = 5;
        this.globalAlpha = 0.8;
        this.cellPadding = 2;

        this._resizeDebounce = this._resizeDebounce.bind(this);

        useEffect(
            () => {
                if (this._ready) {
                    this._render();
                }
            },
            () => [this.props.record.data[this.props.name]]
        );

        onMounted(() => {
            browser.addEventListener("resize", this._resizeDebounce);
            this._ready = true;
            this._resizeDebounce();
        });

        onWillDestroy(() => {
            browser.removeEventListener("resize", this._resizeDebounce);
        });
    }

    get canvas() {
        return this.canvasRef.el;
    }

    get isSet() {
        const value = this.props.record.data[this.props.name];
        return value && Object.keys(value).length > 0 && value.cells?.length > 0;
    }

    get clickAction() {
        return this.props.options?.click_action;
    }

    async _onClick(ev) {
        if (!this.isSet || !this.props.clickAction) {
            return;
        }

        const width = this.canvas.width;
        const height = this.canvas.height;
        const rect = this.canvas.getBoundingClientRect();

        const clickX = ev.clientX - rect.left;
        const clickY = ev.clientY - rect.top;

        const cells = this.props.record.data[this.props.name].cells;
        const cols = cells[0].length;
        const rows = cells.length;

        // We remove 1 to start counting from 0
        let coordX = Math.ceil((clickX * cols) / width) - 1;
        let coordY = Math.ceil((clickY * rows) / height) - 1;

        // If we click on the last pixel on the bottom or the right
        // we would get an offset index
        coordX = Math.min(Math.max(coordX, 0), cols - 1);
        coordY = Math.min(Math.max(coordY, 0), rows - 1);

        // The coordinate we get when we click is from top,
        // but we are looking for the coordinate from the bottom
        // to match the user's expectations, invert Y
        coordY = Math.abs(coordY - rows + 1);
        const action = await this.orm.call(
            this.props.record.resModel,
            this.props.clickAction,
            [[this.props.record.resId], coordX, coordY],
            {}
        );

        await this.action.doAction(action);
    }

    _resizeDebounce() {
        browser.clearTimeout(this._resizePromise);
        this._resizePromise = browser.setTimeout(() => this._render(), 20);
    }

    /**
     * Resize the canvas width and height to the actual size.
     * If we don't do that, it will automatically scale to the
     * CSS size with blurry squares.
     *
     * @param {HTMLElement} canvas - the DOM canvas to draw
     * @returns {Boolean}
     */
    resizeCanvasToDisplaySize(canvas) {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;

        if (canvas.width !== width || canvas.height !== height) {
            canvas.width = width;
            canvas.height = height;
            return true;
        }
        return false;
    }

    /**
     * Render the widget only when it is in the DOM.
     * We need the width and height of the widget to draw the canvas.
     */
    _render() {
        if (!this._ready || !this.canvas) {
            return;
        }

        const ctx = this.canvas.getContext("2d");
        this.resizeCanvasToDisplaySize(ctx.canvas);
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.save();

        if (this.isSet) {
            const value = this.props.record.data[this.props.name];
            const selected = value.selected || [];
            const cells = value.cells;
            this._drawMatrix(this.canvas, ctx, cells, selected);
        }
    }

    /**
     * Draw the cells in the canvas.
     *
     * @param {HTMLElement} canvas - the DOM canvas to draw
     * @param {Object} ctx - the canvas 2d context
     * @param {Array} cells - A 2-dimensional list of cells
     * @param {Array} selected - A list containing the position (x,y) of the
     * selected cell (can be empty if no cell is selected)
     */
    _drawMatrix(canvas, ctx, cells, selected) {
        const colors = {
            0: this.cellColorEmpty,
            1: this.cellColorNotEmpty,
        };

        const cols = cells[0].length;
        const rows = cells.length;
        let selectedX = null;
        let selectedY = null;

        if (selected.length) {
            selectedX = selected[0];
            // We draw top to bottom, but the highlighted cell should
            // be a coordinate from bottom to top: reverse the y axis
            selectedY = Math.abs(selected[1] - rows + 1);
        }

        const padding = this.cellPadding;
        const padding_width = padding * cols;
        const padding_height = padding * rows;
        const w = (canvas.width - padding_width) / cols;
        const h = (canvas.height - padding_height) / rows;

        ctx.globalAlpha = this.globalAlpha;
        // Again, our matrix is top to bottom (0 is the first line)
        // but visually, we want them bottom to top
        const reversed_cells = cells.slice().reverse();

        for (let y = 0; y < rows; y++) {
            for (let x = 0; x < cols; x++) {
                ctx.fillStyle = colors[reversed_cells[y][x]];
                let fillWidth = w;
                let fillHeight = h;

                // Cheat: remove the padding at bottom and right
                // the cells will be a bit larger but not really noticeable
                if (x === cols - 1) {
                    fillWidth += padding;
                }
                if (y === rows - 1) {
                    fillHeight += padding;
                }

                ctx.fillRect(
                    x * (w + padding),
                    y * (h + padding),
                    fillWidth,
                    fillHeight
                );

                if (selected && selectedX === x && selectedY === y) {
                    ctx.globalAlpha = 1.0;
                    ctx.strokeStyle = this.selectedColor;
                    ctx.lineWidth = this.selectedLineWidth;
                    ctx.strokeRect(x * (w + padding), y * (h + padding), w, h);
                    ctx.globalAlpha = this.globalAlpha;
                }
            }
        }
        ctx.restore();
    }
}

export const locationTrayMatrixField = {
    component: LocationTrayMatrixField,
    supportedOptions: [
        {
            name: "click_action",
            type: "string",
        },
    ],
    supportedTypes: ["serialized"],
    extractProps({options}) {
        return {
            clickAction: options.click_action,
        };
    },
};

registry.category("fields").add("location_tray_matrix", locationTrayMatrixField);
