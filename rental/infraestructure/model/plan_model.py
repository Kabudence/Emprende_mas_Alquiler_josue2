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

class PlanPlanModel(Model):
    parent_plan_id = IntegerField()
    child_plan_id  = IntegerField()

    class Meta:
        database    = db
        table_name  = 'plan_plan'
        primary_key = CompositeKey('parent_plan_id', 'child_plan_id')
        indexes = (
            (('parent_plan_id', 'child_plan_id'), True),  # índice único compuesto
        )