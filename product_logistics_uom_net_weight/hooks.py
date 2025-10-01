# Copyright 2025 Factor Libre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    Pre-init hook to migrate net_weight data to product_net_weight field.

    This migration performs a direct copy without UoM conversion because:

    1. **Architectural Analysis**: Before this module, it was impossible to have
       net_weight values in a UoM different from the system's base UoM:
       - Without product_logistics_uom: Products always use system UoM for weight
       - With product_logistics_uom: Only display changes, storage remains in system UoM

    2. **Data Integrity**: Existing net_weight values are guaranteed to be in the
       system's base UoM, making direct migration safe and correct.

    3. **Post-Installation Handling**: After module installation, the computed
       fields will automatically handle proper UoM conversions for new data
       entry and display.

    4. **Performance**: Direct SQL migration is much faster than relying on
       computed field recalculation for databases with many existing products.

    This approach ensures data consistency while maintaining optimal performance
    during the migration process.
    """

    # Add product_net_weight column to product_template
    cr.execute(
        """
        ALTER TABLE product_template
        ADD COLUMN IF NOT EXISTS product_net_weight DOUBLE PRECISION
    """
    )

    cr.execute(
        """
        UPDATE product_template
        SET product_net_weight = net_weight
        WHERE net_weight IS NOT NULL
        AND net_weight > 0
    """
    )
