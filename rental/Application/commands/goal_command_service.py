from rental.domain.entities.goal import Goal
from rental.infraestructure.Repositories.goal_repository import GoalRepository


class GoalCommandService:
    def __init__(self, goal_repo: GoalRepository):
        self.goal_repo = goal_repo

    def create(self, number_of_clients: int, month: int, percentage_to_bonus: float) -> Goal:
        if number_of_clients is None or month is None or percentage_to_bonus is None:
            raise ValueError("All fields are required.")
        goal = Goal(
            number_of_clients=number_of_clients,
            month=month,
            percentage_to_bonus=percentage_to_bonus
        )
        return self.goal_repo.create(goal)

    def update(self, goal_id: int, number_of_clients: int, month: int, percentage_to_bonus: float) -> Goal:
        goal = self.goal_repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Goal not found")
        goal.number_of_clients = number_of_clients
        goal.month = month
        goal.percentage_to_bonus = percentage_to_bonus
        return self.goal_repo.update(goal)

    def delete(self, goal_id: int) -> bool:
        return self.goal_repo.delete(goal_id)
