# Copyright 2025 Opener B.V. (<http://opener.amsterdam>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    """Prevent violation of act_window_view_unique_mode_per_action.

    Violation was triggered after rename of ir.actions.act_window.view in XML.
    """
    cr.execute(
        """
        update ir_model_data
        set name = 'act_open_base_substate_type_view_list'
        where name = 'act_open_base_substate_type_view_tree'
             and module = 'base_substate';
        update ir_model_data
        set name = 'act_open_target_state_value_view_list'
        where name = 'act_open_target_state_value_view_tree'
             and module = 'base_substate';
        update ir_model_data
        set name = 'act_open_base_substate_view_list'
        where name = 'act_open_base_substate_view_tree'
             and module = 'base_substate';
        """
    )
