# plans/infrastructure/models/plan_model.py
from peewee import Model, AutoField, CharField, FloatField
from shared.infrastructure.database import db

class PlanModel(Model):
    id          = AutoField(primary_key=True)
    name        = CharField(null=False)
    description = CharField(null=False)
    price       = FloatField(null=False)

    class Meta:
        database   = db
        table_name = 'plans'
        indexes    = (
            (('name',), False),  # Ejemplo: podrías poner unique si los nombres deben ser únicos
        )
