# Copyright (c) 2019-2022 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPL 3.0: https://www.gnu.org/licenses/gpl-3.0.txt

from django.db import models
from django.contrib.postgres.indexes import GinIndex


class Purchase(models.Model):
    """
    Holds information about GitHub ``marketplace_purchase`` events:
    https://developer.github.com/marketplace/integrating-with-the-github-marketplace-api/github-marketplace-webhook-events/
    """

    vendor = models.CharField(max_length=16, db_index=True, blank=True, null=True)
    action = models.CharField(max_length=64, db_index=True)
    sender = models.EmailField(db_index=True)
    subscription = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    effective_date = models.DateTimeField(db_index=True)
    should_have_tenant = models.BooleanField(default=False, db_index=True)
    should_have_support = models.BooleanField(default=False, db_index=True)

    # this is for internal purposes
    received_on = models.DateTimeField(db_index=True, auto_now_add=True)

    payload = models.JSONField()

    class Meta:
        indexes = [
            GinIndex(
                fastupdate=False, fields=["payload"], name="tcms_github_payload_gin"
            ),
        ]

    def __str__(self):
        return f"Purchase {self.action} from {self.sender} on {self.received_on.isoformat()}"
