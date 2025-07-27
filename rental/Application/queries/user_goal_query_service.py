from typing import List, Optional
from rental.domain.entities.user_goal import UserGoal
from rental.infraestructure.Repositories.user_goal_repository import UserGoalRepository


class UserGoalQueryService:
    def __init__(self, user_goal_repo: UserGoalRepository):
        self.user_goal_repo = user_goal_repo

    def get_by_id(self, user_goal_id: int) -> Optional[UserGoal]:
        return self.user_goal_repo.get_by_id(user_goal_id)

    def list_all(self) -> List[UserGoal]:
        return self.user_goal_repo.get_all()

    def list_by_user(self, user_id: int) -> List[UserGoal]:
        # Este método debes agregarlo a tu UserGoalRepository
        return self.user_goal_repo.get_by_user(user_id)

    def list_by_goal(self, goal_id: int) -> List[UserGoal]:
        # Este método también lo agregas al repo si lo necesitas
        return self.user_goal_repo.get_by_goal(goal_id)
