# user_goals/infrastructure/models/user_goal_model.py
from peewee import Model, AutoField, IntegerField, BooleanField, DateTimeField
from shared.infrastructure.database import db

class UserGoalModel(Model):
    id            = AutoField(primary_key=True)
    user_id       = IntegerField(null=False)
    goal_id       = IntegerField(null=False)
    goal_attained = BooleanField(default=False)
    initial_date  = DateTimeField(null=True)  # Puedes usar null=True si a veces viene vacío

    class Meta:
        database   = db
        table_name = 'user_goals'
        indexes    = (
            (('user_id', 'goal_id'), False),  # Puedes cambiar a True si quieres evitar duplicados por usuario/objetivo
        )
