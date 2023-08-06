"""Google Models class file."""

from billing_account import BillingAccount


class Models(object):
    """Google Models class."""

    def __init__(self, google=None):
        """Initialize a Google Models instance."""
        self.google = google

    def billing_account(self):
        """Return a Google Billing Account."""
        return BillingAccount(self.google)
