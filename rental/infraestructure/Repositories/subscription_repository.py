from typing import Optional, List
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rental.domain.entities.subscription import Subscription, SubscriptionStatus
from rental.infraestructure.model.subscription_model import SubscriptionModel


class SubscriptionRepository:
    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))  # Fijo UTC-5 para Lima

    @staticmethod
    def _iso_to_datetime(iso_str: str) -> datetime:
        tz_lima = SubscriptionRepository._safe_zoneinfo("America/Lima")
        return datetime.strptime(iso_str, "%Y-%m-%d").replace(tzinfo=tz_lima)


    def get_by_id(self, id: int) -> Optional[Subscription]:
        try:
            record = SubscriptionModel.get(SubscriptionModel.id == id)
            return Subscription(
                id=record.id,
                plan_id=record.plan_id,
                negocio_id=record.negocio_id,
                initial_date=record.initial_date.isoformat(),
                final_date=record.final_date.isoformat(),
                status=SubscriptionStatus(record.status)
            )
        except SubscriptionModel.DoesNotExist:
            return None

    def get_all(self) -> List[Subscription]:
        return [
            Subscription(
                id=rec.id,
                plan_id=rec.plan_id,
                negocio_id=rec.negocio_id,
                initial_date=rec.initial_date.isoformat(),
                final_date=rec.final_date.isoformat(),
                status=SubscriptionStatus(rec.status)
            )
            for rec in SubscriptionModel.select()
        ]

    def create(self, subscription: Subscription) -> Subscription:
        tz_lima = self._safe_zoneinfo("America/Lima")
        # La fecha de creación es ahora (Lima)
        initial_date = datetime.now(tz_lima)
        # final_date es un mes después
        final_date = initial_date + timedelta(days=30)  # 30 días, para asegurar mes aunque no siempre coincida calendario
        record = SubscriptionModel.create(
            plan_id=subscription.plan_id,
            negocio_id=subscription.negocio_id,
            initial_date=initial_date,
            final_date=final_date,
            status=subscription.status.value if isinstance(subscription.status, SubscriptionStatus) else subscription.status
        )
        return Subscription(
            id=record.id,
            plan_id=record.plan_id,
            negocio_id=record.negocio_id,
            initial_date=record.initial_date.isoformat(),
            final_date=record.final_date.isoformat(),
            status=SubscriptionStatus(record.status)
        )

    def update(self, subscription: Subscription) -> Optional[Subscription]:
        try:
            record = SubscriptionModel.get(SubscriptionModel.id == subscription.id)
            record.plan_id = subscription.plan_id
            record.negocio_id = subscription.negocio_id
            # Si quieres permitir actualizar fechas, agrega esto:
            record.initial_date = self._iso_to_datetime(subscription.initial_date)
            record.final_date = self._iso_to_datetime(subscription.final_date)
            record.status = subscription.status.value if isinstance(subscription.status, SubscriptionStatus) else subscription.status
            record.save()
            return Subscription(
                id=record.id,
                plan_id=record.plan_id,
                negocio_id=record.negocio_id,
                initial_date=record.initial_date.isoformat(),
                final_date=record.final_date.isoformat(),
                status=SubscriptionStatus(record.status)
            )
        except SubscriptionModel.DoesNotExist:
            return None

    def delete(self, subscription_id: int) -> bool:
        try:
            record = SubscriptionModel.get(SubscriptionModel.id == subscription_id)
            record.delete_instance()
            return True
        except SubscriptionModel.DoesNotExist:
            return False

    def get_by_negocio(self, negocio_id: int) -> List[Subscription]:
        """
        Devuelve todas las suscripciones de un negocio.
        """
        return [
            Subscription(
                id=rec.id,
                plan_id=rec.plan_id,
                negocio_id=rec.negocio_id,
                initial_date=rec.initial_date.isoformat(),
                final_date=rec.final_date.isoformat(),
                status=SubscriptionStatus(rec.status)
            )
            for rec in SubscriptionModel.select().where(SubscriptionModel.negocio_id == negocio_id)
        ]

    def get_by_status(self, status: str) -> List[Subscription]:
        """
        Devuelve todas las suscripciones con cierto estado ('active', 'inactive', etc).
        """
        return [
            Subscription(
                id=rec.id,
                plan_id=rec.plan_id,
                negocio_id=rec.negocio_id,
                initial_date=rec.initial_date.isoformat(),
                final_date=rec.final_date.isoformat(),
                status=SubscriptionStatus(rec.status)
            )
            for rec in SubscriptionModel.select().where(SubscriptionModel.status == status)
        ]