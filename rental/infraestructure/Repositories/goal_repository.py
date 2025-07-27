from typing import Optional, List

from rental.domain.entities.goal import Goal
from rental.infraestructure.model.goal_model import GoalModel


class GoalRepository:
    def get_by_id(self, id: int) -> Optional[Goal]:
        try:
            record = GoalModel.get(GoalModel.id == id)
            return Goal(
                id=record.id,
                number_of_clients=record.number_of_clients,
                month=record.month,
                percentage_to_bonus=record.percentage_to_bonus
            )
        except GoalModel.DoesNotExist:
            return None

    def get_all(self) -> List[Goal]:
        return [
            Goal(
                id=rec.id,
                number_of_clients=rec.number_of_clients,
                month=rec.month,
                percentage_to_bonus=rec.percentage_to_bonus
            )
            for rec in GoalModel.select()
        ]

    def create(self, goal: Goal) -> Goal:
        record = GoalModel.create(
            number_of_clients=goal.number_of_clients,
            month=goal.month,
            percentage_to_bonus=goal.percentage_to_bonus
        )
        return Goal(
            id=record.id,
            number_of_clients=record.number_of_clients,
            month=record.month,
            percentage_to_bonus=record.percentage_to_bonus
        )

    def update(self, goal: Goal) -> Optional[Goal]:
        try:
            record = GoalModel.get(GoalModel.id == goal.id)
            record.number_of_clients = goal.number_of_clients
            record.month = goal.month
            record.percentage_to_bonus = goal.percentage_to_bonus
            record.save()
            return Goal(
                id=record.id,
                number_of_clients=record.number_of_clients,
                month=record.month,
                percentage_to_bonus=record.percentage_to_bonus
            )
        except GoalModel.DoesNotExist:
            return None

    def delete(self, goal_id: int) -> bool:
        try:
            record = GoalModel.get(GoalModel.id == goal_id)
            record.delete_instance()
            return True
        except GoalModel.DoesNotExist:
            return False
