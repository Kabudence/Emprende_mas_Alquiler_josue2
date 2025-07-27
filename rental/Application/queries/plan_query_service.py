from typing import List, Optional

from rental.domain.entities.plan import Plan
from rental.infraestructure.Repositories.plan_repository import PlanRepository


class PlanQueryService:
    def __init__(self, plan_repo: PlanRepository):
        self.plan_repo = plan_repo

    def get_by_id(self, plan_id: int) -> Optional[Plan]:
        return self.plan_repo.get_by_id(plan_id)

    def list_all(self) -> List[Plan]:
        return self.plan_repo.get_all()


