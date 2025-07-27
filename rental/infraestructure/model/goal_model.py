from peewee import Model, AutoField, IntegerField, FloatField
from shared.infrastructure.database import db

class GoalModel(Model):
    id                  = AutoField(primary_key=True)
    number_of_clients   = IntegerField(null=False)
    month               = IntegerField(null=False)   # Usualmente un valor del 1 al 12
    percentage_to_bonus = FloatField(null=False)

    class Meta:
        database   = db
        table_name = 'goals'
        indexes    = (
            (('month',), False),
        )
