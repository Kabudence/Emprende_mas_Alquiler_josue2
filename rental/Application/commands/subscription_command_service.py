from rental.domain.entities.subscription import Subscription, SubscriptionStatus
from rental.infraestructure.Repositories.subscription_repository import SubscriptionRepository


class SubscriptionCommandService:
    def __init__(self, subscription_repo: SubscriptionRepository):
        self.subscription_repo = subscription_repo

    def create(self, plan_id: int, user_id: int, status: SubscriptionStatus = SubscriptionStatus.ACTIVE) -> Subscription:
        if plan_id is None or user_id is None:
            raise ValueError("plan_id and user_id are required.")
        subscription = Subscription(
            plan_id=plan_id,
            user_id=user_id,
            initial_date="",   # Se ignora; lo setea el repo con la hora actual
            final_date="",     # Se ignora; lo setea el repo con la hora actual + 1 mes
            status=status
        )
        return self.subscription_repo.create(subscription)

    def update(self, subscription_id: int, plan_id: int, user_id: int, initial_date: str, final_date: str, status: SubscriptionStatus) -> Subscription:
        subscription = self.subscription_repo.get_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        subscription.plan_id = plan_id
        subscription.user_id = user_id
        subscription.initial_date = initial_date
        subscription.final_date = final_date
        subscription.status = status
        return self.subscription_repo.update(subscription)

    def delete(self, subscription_id: int) -> bool:
        return self.subscription_repo.delete(subscription_id)
