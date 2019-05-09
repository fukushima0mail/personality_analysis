from django.db import models
from django.utils import timezone


class Group(models.Model):
    group_cd = models.CharField(primary_key=True, max_length=2, null=False)
    group_nm = models.CharField(max_length=60, null=False)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.group_cd
