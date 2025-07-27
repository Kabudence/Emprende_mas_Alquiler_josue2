from typing import List, Optional
from rental.domain.entities.commissions import Commissions
from rental.infraestructure.Repositories.commissions_repository import CommissionRepository
from rental.infraestructure.model.commissions_model import CommissionModel

class CommissionQueryService:
    def __init__(self, commission_repo: CommissionRepository):
        self.commission_repo = commission_repo

    def get_by_id(self, commission_id: int) -> Optional[Commissions]:
        return self.commission_repo.get_by_id(commission_id)

    def list_all(self) -> List[Commissions]:
        return self.commission_repo.get_all()

    def list_by_user_id(self, user_id: int) -> List[Commissions]:
        return self.commission_repo.get_all_by_user_id(user_id)

    def list_by_subscription_id(self, subscription_id: int) -> List[Commissions]:
        return [
            Commissions(
                id=rec.id,
                user_id=rec.user_id,
                subscription_id=rec.subscription_id if rec.subscription_id is not None else None,
                amount=rec.amount,
                type=rec.type,
                created_at=rec.created_at.isoformat() if rec.created_at else None
            )
            for rec in CommissionModel.select().where(CommissionModel.subscription_id == subscription_id)
        ]
