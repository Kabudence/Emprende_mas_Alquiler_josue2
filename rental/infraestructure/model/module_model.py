# modules/infrastructure/models/module_model.py
from peewee import Model, AutoField, CharField
from shared.infrastructure.database import db

class ModuleModel(Model):
    id          = AutoField(primary_key=True)
    name        = CharField(null=False)
    description = CharField(null=False)

    class Meta:
        database   = db
        table_name = 'modules'
        indexes    = (
            (('name',), False),  # Puedes ponerlo en True si deseas que name sea único
        )

