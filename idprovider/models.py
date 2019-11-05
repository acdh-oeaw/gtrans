from django.db import models


class IdProvider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked = models.BooleanField(
        verbose_name="checked",
        help_text="Check if everything is ok",
        default=False
    )

    class Meta:
        ordering = ('id', )
