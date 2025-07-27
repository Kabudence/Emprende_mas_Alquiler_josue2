from typing import Optional, List
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rental.domain.entities.commissions import Commissions
from rental.infraestructure.model.commissions_model import CommissionModel


class CommissionRepository:
    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))  # UTC-5 Lima

    def get_by_id(self, id: int) -> Optional[Commissions]:
        try:
            record = CommissionModel.get(CommissionModel.id == id)
            return Commissions(
                id=record.id,
                user_id=record.user_id,
                subscription_id=record.subscription_id if record.subscription_id is not None else None,
                amount=record.amount,
                type=record.type,
                created_at=record.created_at.isoformat() if record.created_at else None
            )
        except CommissionModel.DoesNotExist:
            return None

    def get_all(self) -> List[Commissions]:
        return [
            Commissions(
                id=rec.id,
                user_id=rec.user_id,
                subscription_id=rec.subscription_id if rec.subscription_id is not None else None,
                amount=rec.amount,
                type=rec.type,
                created_at=rec.created_at.isoformat() if rec.created_at else None
            )
            for rec in CommissionModel.select()
        ]

    def create(self, commission: Commissions) -> Commissions:
        tz_lima = self._safe_zoneinfo("America/Lima")
        created_at = datetime.now(tz_lima)
        record = CommissionModel.create(
            user_id=commission.user_id,
            subscription_id=commission.subscription_id if commission.subscription_id is not None else None,
            amount=commission.amount,
            type=commission.type,
            created_at=created_at
        )
        return Commissions(
            id=record.id,
            user_id=record.user_id,
            subscription_id=record.subscription_id if record.subscription_id is not None else None,
            amount=record.amount,
            type=record.type,
            created_at=record.created_at.isoformat() if record.created_at else None
        )

    def update(self, commission: Commissions) -> Optional[Commissions]:
        try:
            record = CommissionModel.get(CommissionModel.id == commission.id)
            record.user_id = commission.user_id
            record.subscription_id = commission.subscription_id if commission.subscription_id is not None else None
            record.amount = commission.amount
            record.type = commission.type
            # created_at solo al crear
            record.save()
            return Commissions(
                id=record.id,
                user_id=record.user_id,
                subscription_id=record.subscription_id if record.subscription_id is not None else None,
                amount=record.amount,
                type=record.type,
                created_at=record.created_at.isoformat() if record.created_at else None
            )
        except CommissionModel.DoesNotExist:
            return None

    def delete(self, commission_id: int) -> bool:
        try:
            record = CommissionModel.get(CommissionModel.id == commission_id)
            record.delete_instance()
            return True
        except CommissionModel.DoesNotExist:
            return False


    def get_all_by_user_id(self, user_id: int) -> List[Commissions]:
        return [
            Commissions(
                id=rec.id,
                user_id=rec.user_id,
                subscription_id=rec.subscription_id if rec.subscription_id is not None else None,
                amount=rec.amount,
                type=rec.type,
                created_at=rec.created_at.isoformat() if rec.created_at else None
            )
            for rec in CommissionModel.select().where(CommissionModel.user_id == user_id)
        ]
