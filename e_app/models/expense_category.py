from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel


class ExpenseCategory(GenericBaseModel):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=2555, null=True)

    def __str__(self):
        return self.name
