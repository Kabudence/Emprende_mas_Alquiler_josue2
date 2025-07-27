from typing import Optional

from rental.domain.entities.commissions import Commissions, CommissionsTypes
from rental.infraestructure.Repositories.commissions_repository import CommissionRepository


class CommissionCommandService:
    def __init__(self, commission_repo: CommissionRepository):
        self.commission_repo = commission_repo

    def create(
            self,
            user_id: int,
            amount: float,
            type: str = CommissionsTypes,
            subscription_id: int = None ) -> Commissions:
        if user_id is None or amount is None or type is None:
            raise ValueError("user_id, amount and type are required")

        # Soporta que type venga como string ("direct"/"referred") o como Enum
        if isinstance(type, str):
            if type not in (CommissionsTypes.DIRECT, CommissionsTypes.REFERRED):
                raise ValueError("type must be 'direct' or 'referred'")
            type_enum = type
        else:
            type_enum = type if type in (
            CommissionsTypes.DIRECT, CommissionsTypes.REFERRED) else CommissionsTypes.DIRECT

        commission = Commissions(
            user_id=user_id,
            subscription_id=subscription_id,
            amount=amount,
            type=type_enum
        )
        return self.commission_repo.create(commission)

    def update(
            self,
            commission_id: int,
            user_id: int,
            amount: float,
            type: str = CommissionsTypes.DIRECT,
            subscription_id: int = None
    ) -> Optional[Commissions]:
        commission = self.commission_repo.get_by_id(commission_id)
        if not commission:
            raise ValueError("Commission not found")

        # Validar tipo de comisión
        if isinstance(type, str):
            if type not in (CommissionsTypes.DIRECT, CommissionsTypes.REFERRED):
                raise ValueError("type must be 'direct' or 'referred'")
            type_enum = type
        else:
            type_enum = type if type in (
            CommissionsTypes.DIRECT, CommissionsTypes.REFERRED) else CommissionsTypes.DIRECT

        commission.user_id = user_id
        commission.amount = amount
        commission.type = type_enum
        commission.subscription_id = subscription_id
        return self.commission_repo.update(commission)


    def delete(self, commission_id: int) -> bool:
        return self.commission_repo.delete(commission_id)
