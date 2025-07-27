from typing import Optional, List
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rental.domain.entities.payment import Payment, PaymentStatus
from rental.infraestructure.model.payment_model import PaymentModel


class PaymentRepository:
    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))  # UTC-5 Lima

    def get_by_id(self, id: int) -> Optional[Payment]:
        try:
            record = PaymentModel.get(PaymentModel.id == id)
            return Payment(
                id=record.id,
                user_id=record.user_id,
                amount=record.amount,
                created_at=record.created_at.isoformat(),
                status=PaymentStatus(record.status)
            )
        except PaymentModel.DoesNotExist:
            return None

    def get_all(self) -> List[Payment]:
        return [
            Payment(
                id=rec.id,
                user_id=rec.user_id,
                amount=rec.amount,
                created_at=rec.created_at.isoformat(),
                status=PaymentStatus(rec.status)
            )
            for rec in PaymentModel.select()
        ]

    def create(self, payment: Payment) -> Payment:
        tz_lima = self._safe_zoneinfo("America/Lima")
        created_at = datetime.now(tz_lima)
        record = PaymentModel.create(
            user_id=payment.user_id,
            amount=payment.amount,
            created_at=created_at,
            status=payment.status.value if isinstance(payment.status, PaymentStatus) else payment.status
        )
        return Payment(
            id=record.id,
            user_id=record.user_id,
            amount=record.amount,
            created_at=record.created_at.isoformat(),
            status=PaymentStatus(record.status)
        )

    def update(self, payment: Payment) -> Optional[Payment]:
        try:
            record = PaymentModel.get(PaymentModel.id == payment.id)
            record.user_id = payment.user_id
            record.amount = payment.amount
            # No suele permitirse cambiar created_at, pero si necesitas, puedes habilitar:
            # record.created_at = self._iso_to_datetime(payment.created_at)
            record.status = payment.status.value if isinstance(payment.status, PaymentStatus) else payment.status
            record.save()
            return Payment(
                id=record.id,
                user_id=record.user_id,
                amount=record.amount,
                created_at=record.created_at.isoformat(),
                status=PaymentStatus(record.status)
            )
        except PaymentModel.DoesNotExist:
            return None

    def delete(self, payment_id: int) -> bool:
        try:
            record = PaymentModel.get(PaymentModel.id == payment_id)
            record.delete_instance()
            return True
        except PaymentModel.DoesNotExist:
            return False
