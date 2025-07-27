from typing import List, Optional
from rental.domain.entities.goal import Goal
from rental.infraestructure.Repositories.goal_repository import GoalRepository


class GoalQueryService:
    def __init__(self, goal_repo: GoalRepository):
        self.goal_repo = goal_repo

    def get_by_id(self, goal_id: int) -> Optional[Goal]:
        return self.goal_repo.get_by_id(goal_id)

    def list_all(self) -> List[Goal]:
        return self.goal_repo.get_all()

    # def get_by_month(self, month: int) -> List[Goal]:
    #     # Supone que agregas este método en tu GoalRepository:
    #     return self.goal_repo.get_by_month(month)
