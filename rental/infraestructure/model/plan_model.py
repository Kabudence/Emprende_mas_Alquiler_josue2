# plans/infrastructure/models/plan_model.py
from peewee import Model, AutoField, CharField, FloatField, IntegerField, CompositeKey
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

class PlanModuleModel(Model):
    plan_id = IntegerField()
    module_id  = IntegerField()

    class Meta:
        database    = db
        table_name  = 'plan_modules'
        primary_key = CompositeKey('plan_id', 'module_id')
        indexes = (
            (('plan_id', 'module_id'), True),  # índice único compuesto
        )