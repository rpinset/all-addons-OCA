/** @odoo-module **/
import {ProgressBarField} from "@web/views/fields/progress_bar/progress_bar_field";
import {registry} from "@web/core/registry";

// Get the existing progressbar field definition from the registry
const progressbarField = registry.category("fields").get("progressbar");

class ProgressBarFractionalField extends ProgressBarField {
    // Extend original field props with a new optional prop
    static props = {
        ...ProgressBarField.props,
        showFractional: {type: Boolean, optional: true},
    };

    // Inherit format logic to support custom fractional rendering.
    formatCurrentValue(humanReadable = !this.state.isEditing) {
        // Customization Start
        const value = this.currentValue || 0;
        const max = this.maxValue || 100;
        if (this.props.showFractional || max !== 100) {
            const formatters = registry.category("formatters");
            const humanValue = formatters.get(
                Number.isInteger(value) ? "integer" : "float"
            )(value, {humanReadable});
            const humanMax = formatters.get(
                Number.isInteger(max) ? "integer" : "float"
            )(max, {humanReadable});
            return `${humanValue} / ${humanMax}`;
            // Customization End
        }
        return super.formatCurrentValue(humanReadable);
    }
}

progressbarField.component = ProgressBarFractionalField;
// Add a new option show_fractional
progressbarField.supportedOptions.push({
    label: "Show fractional",
    name: "show_fractional",
    type: "boolean",
});

// ExtractProps to pass the show_fractional option into the component props
const originalExtract = progressbarField.extractProps;
progressbarField.extractProps = ({attrs, options}) => ({
    ...originalExtract({attrs, options}),
    showFractional: options.show_fractional || false,
});
