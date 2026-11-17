# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


def hoot_id(name):
    """HOOT job id of a test suite, as the test runner computes it."""
    value = 0
    for char in name:
        value = ((value << 5) - value + ord(char)) & 0xFFFFFFFF
    return f"{value:08x}"


@tagged("post_install", "-at_install")
class TestTierReviewWidgetForward(HttpCase):
    def test_tier_review_widget_forward(self):
        self.browser_js(
            "/web/tests?headless&loglevel=2&preset=desktop&timeout=15000"
            f"&id={hoot_id('@base_tier_validation_forward/tier_review_widget_forward')}",
            "",
            "",
            login="admin",
            timeout=1800,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=lambda message: "[HOOT]" not in message,
        )
