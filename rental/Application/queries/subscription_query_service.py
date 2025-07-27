from typing import List, Optional
from rental.domain.entities.subscription import Subscription
from rental.infraestructure.Repositories.subscription_repository import SubscriptionRepository


class SubscriptionQueryService:
    def __init__(self, subscription_repo: SubscriptionRepository):
        self.subscription_repo = subscription_repo

    def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        return self.subscription_repo.get_by_id(subscription_id)

    def list_all(self) -> List[Subscription]:
        return self.subscription_repo.get_all()

    def list_by_user(self, user_id: int) -> List[Subscription]:
        # Debes agregar este método en tu repo si aún no lo tienes
        return self.subscription_repo.get_by_user(user_id)

    def list_by_status(self, status: str) -> List[Subscription]:
        # También agrega esto en tu repo si lo usas mucho
        return self.subscription_repo.get_by_status(status)
