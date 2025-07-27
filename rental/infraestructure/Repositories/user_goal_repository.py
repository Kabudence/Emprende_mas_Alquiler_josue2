from typing import Optional, List
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rental.domain.entities.user_goal import UserGoal
from rental.infraestructure.model.user_goal_model import UserGoalModel


class UserGoalRepository:
    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))  # UTC-5 Lima

    def get_by_id(self, id: int) -> Optional[UserGoal]:
        try:
            record = UserGoalModel.get(UserGoalModel.id == id)
            return UserGoal(
                id=record.id,
                user_id=record.user_id,
                goal_id=record.goal_id,
                goal_attained=record.goal_attained,
                initial_date=record.initial_date.isoformat() if record.initial_date else None
            )
        except UserGoalModel.DoesNotExist:
            return None

    def get_all(self) -> List[UserGoal]:
        return [
            UserGoal(
                id=rec.id,
                user_id=rec.user_id,
                goal_id=rec.goal_id,
                goal_attained=rec.goal_attained,
                initial_date=rec.initial_date.isoformat() if rec.initial_date else None
            )
            for rec in UserGoalModel.select()
        ]

    def create(self, user_goal: UserGoal) -> UserGoal:
        tz_lima = self._safe_zoneinfo("America/Lima")
        initial_date = datetime.now(tz_lima)
        record = UserGoalModel.create(
            user_id=user_goal.user_id,
            goal_id=user_goal.goal_id,
            goal_attained=False,
            initial_date=initial_date
        )
        return UserGoal(
            id=record.id,
            user_id=record.user_id,
            goal_id=record.goal_id,
            goal_attained=record.goal_attained,
            initial_date=record.initial_date.isoformat() if record.initial_date else None
        )

    def update(self, user_goal: UserGoal) -> Optional[UserGoal]:
        try:
            record = UserGoalModel.get(UserGoalModel.id == user_goal.id)
            record.user_id = user_goal.user_id
            record.goal_id = user_goal.goal_id
            record.goal_attained = user_goal.goal_attained
            # Normalmente no se cambia initial_date, pero puedes permitirlo así:
            # record.initial_date = self._iso_to_datetime(user_goal.initial_date) if user_goal.initial_date else None
            record.save()
            return UserGoal(
                id=record.id,
                user_id=record.user_id,
                goal_id=record.goal_id,
                goal_attained=record.goal_attained,
                initial_date=record.initial_date.isoformat() if record.initial_date else None
            )
        except UserGoalModel.DoesNotExist:
            return None

    def delete(self, user_goal_id: int) -> bool:
        try:
            record = UserGoalModel.get(UserGoalModel.id == user_goal_id)
            record.delete_instance()
            return True
        except UserGoalModel.DoesNotExist:
            return False

    def get_by_user(self, user_id: int) -> List[UserGoal]:
        return [
            UserGoal(
                id=rec.id,
                user_id=rec.user_id,
                goal_id=rec.goal_id,
                goal_attained=rec.goal_attained,
                initial_date=rec.initial_date.isoformat() if rec.initial_date else None
            )
            for rec in UserGoalModel.select().where(UserGoalModel.user_id == user_id)
        ]

    def get_by_goal(self, goal_id: int) -> List[UserGoal]:
        return [
            UserGoal(
                id=rec.id,
                user_id=rec.user_id,
                goal_id=rec.goal_id,
                goal_attained=rec.goal_attained,
                initial_date=rec.initial_date.isoformat() if rec.initial_date else None
            )
            for rec in UserGoalModel.select().where(UserGoalModel.goal_id == goal_id)
        ]
