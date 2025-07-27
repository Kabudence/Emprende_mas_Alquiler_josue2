# payments/infrastructure/models/payment_model.py
from peewee import Model, AutoField, IntegerField, FloatField, DateTimeField, CharField

from rental.domain.entities.payment import PaymentStatus
from shared.infrastructure.database import db

class PaymentModel(Model):
    id         = AutoField(primary_key=True)
    user_id    = IntegerField(null=False)
    amount     = FloatField(null=False)
    created_at = DateTimeField(null=False)
    status     = CharField(
        max_length=20,
        default=PaymentStatus.PENDING.value,
        choices=[(status.value, status.value) for status in PaymentStatus]
    )

    class Meta:
        database   = db
        table_name = 'payments'
        indexes    = (
            (('user_id', 'status'), False),
        )

