from peewee import Model, AutoField, IntegerField, DateTimeField, CharField

from rental.domain.entities.subscription import SubscriptionStatus
from shared.infrastructure.database import db

class SubscriptionModel(Model):
    id           = AutoField(primary_key=True)
    plan_id      = IntegerField(null=False)
    negocio_id   = IntegerField(null=False)
    initial_date = DateTimeField(null=False)
    final_date   = DateTimeField(null=False)
    status       = CharField(
        max_length=20,
        default=SubscriptionStatus.ACTIVE.value,
        choices=[(status.value, status.value) for status in SubscriptionStatus]
    )

    class Meta:
        database   = db
        table_name = 'subscriptions'
        indexes    = (
            (('plan_id', 'negocio_id'), False),
        )
