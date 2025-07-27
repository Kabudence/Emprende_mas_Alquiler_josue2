from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.models import Usuario
from rental.domain.entities.commissions import CommissionsTypes
from rental.domain.entities.subscription import SubscriptionStatus

class UserFlowService:
    def __init__(
        self,
        user_goal_command_service,
        subscription_command_service,
        commission_command_service,
        plan_query_service
    ):
        self.user_goal_command_service = user_goal_command_service
        self.subscription_command_service = subscription_command_service
        self.commission_command_service = commission_command_service
        self.plan_query_service = plan_query_service

    @staticmethod
    def _safe_zoneinfo(key: str):
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            return timezone(timedelta(hours=-5))  # UTC-5 Lima

    def seller_user_flow(self, user_id: int):
        user = Usuario.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if user.role != "AFILIADO":
            raise ValueError("User must have role 'AFILIADO'")

        # Crear meta para el usuario (goal_id=1)
        return self.user_goal_command_service.create(user_id=user_id, goal_id=1)


    def buyer_user_flow(self, user_id: int, plan_id: int):
        user = Usuario.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if user.role != "COMPRADOR":
            raise ValueError("User must have role 'COMPRADOR'")

        # Crear suscripción
        subscription = self.subscription_command_service.create(
            plan_id=plan_id,
            user_id=user_id,
            status=SubscriptionStatus.ACTIVE
        )

        # Obtener información del plan para el cálculo de comisión
        plan = self.plan_query_service.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found")

        # Crear comisión para el usuario (tipo DIRECT, monto = 20% del precio del plan)
        commission = self.commission_command_service.create(
            user_id=user_id,
            amount=plan.price * 0.2,
            type=CommissionsTypes.DIRECT,
            subscription_id=subscription.id
        )
        self.validate_state_user_goal(user_id)
        return {
            "subscription": subscription,
            "commission": commission
        }

    def validate_state_user_goal(self, user_id: int):
        # Buscar los goals del usuario
        user_goals = self.user_goal_command_service.list_by_user(user_id)
        if not user_goals:
            return None

        user_goal = user_goals[0]

        # --- USO DE LA FECHA ACTUAL CON ZONA HORARIA LIMA ---
        tz_lima = self._safe_zoneinfo("America/Lima")
        initial_date = (
            datetime.fromisoformat(user_goal.initial_date)
            if isinstance(user_goal.initial_date, str)
            else user_goal.initial_date
        )
        now = datetime.now(tz_lima)

        # Si la diferencia es >= 1 mes (usamos 30 días para simplificar)
        if (now - initial_date).days >= 30:
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            user_goal.initial_date = first_day.isoformat()
            user_goal.goal_attained = False
            self.user_goal_command_service.user_goal_repo.update(user_goal)
            return

        # Si la meta está cumplida (goal_attained == True), salir
        if user_goal.goal_attained:
            return

        # Si la meta no está cumplida, obtener comisiones del usuario
        commissions = self.commission_command_service.commission_repo.get_all_by_user_id(user_id)
        num_commissions = len(commissions)

        # Buscar la meta (goal) a la que apunta este UserGoal
        goal = self.user_goal_command_service.user_goal_repo.goal_repo.get_by_id(user_goal.goal_id)
        if not goal:
            raise ValueError("Goal not found")

        # Si tiene suficientes comisiones, cumplir la meta y otorgar bonificación
        if num_commissions >= goal.number_of_clients:
            user_goal.goal_attained = True
            self.user_goal_command_service.user_goal_repo.update(user_goal)

            # Calcular el monto total de comisiones
            total_amount = sum(c.amount for c in commissions if hasattr(c, 'amount'))

            # (total_amount / 0.2) * percentage_to_bonus
            if goal.percentage_to_bonus is not None:
                reward = (total_amount / 0.2) * goal.percentage_to_bonus
                # Guardar la comisión como REFERRED
                self.commission_command_service.create(
                    user_id=user_id,
                    amount=reward,
                    type=CommissionsTypes.REFERRED,
                    subscription_id=None
                )

