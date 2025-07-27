from rental.domain.entities.user_goal import UserGoal
from rental.infraestructure.Repositories.user_goal_repository import UserGoalRepository


class UserGoalCommandService:
    def __init__(self, user_goal_repo: UserGoalRepository):
        self.user_goal_repo = user_goal_repo

    def create(self, user_id: int, goal_id: int) -> UserGoal:
        if user_id is None or goal_id is None:
            raise ValueError("user_id and goal_id are required")
        user_goal = UserGoal(user_id=user_id, goal_id=goal_id)
        return self.user_goal_repo.create(user_goal)

    def update_attained(self, user_goal_id: int, attained: bool) -> UserGoal:
        user_goal = self.user_goal_repo.get_by_id(user_goal_id)
        if not user_goal:
            raise ValueError("UserGoal not found")
        user_goal.goal_attained = attained
        return self.user_goal_repo.update(user_goal)

    def delete(self, user_goal_id: int) -> bool:
        return self.user_goal_repo.delete(user_goal_id)


