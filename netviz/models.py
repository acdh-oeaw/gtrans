from django.db import models


class NetVisCache(models.Model):
    app_name = models.CharField(blank=True, max_length=250)
    model_name = models.CharField(blank=True, max_length=250)
    updated_at = models.DateTimeField(auto_now=True)
    graph_data = models.TextField(blank=True)

    def __str__(self):
        return f"{self.app_name}__{self.model_name}"
