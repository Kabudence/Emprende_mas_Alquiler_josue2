from typing import Optional, List

from rental.domain.entities.plan import Plan
from rental.infraestructure.model.plan_model import PlanModel


class PlanRepository:
    def get_by_id(self, id: int) -> Optional[Plan]:
        try:
            record = PlanModel.get(PlanModel.id == id)
            return Plan(
                id=record.id,
                name=record.name,
                description=record.description,
                price=record.price
            )
        except PlanModel.DoesNotExist:
            return None

    def get_all(self) -> List[Plan]:
        return [
            Plan(
                id=rec.id,
                name=rec.name,
                description=rec.description,
                price=rec.price
            )
            for rec in PlanModel.select()
        ]

    def create(self, plan: Plan) -> Plan:
        record = PlanModel.create(
            name=plan.name,
            description=plan.description,
            price=plan.price
        )
        return Plan(
            id=record.id,
            name=record.name,
            description=record.description,
            price=record.price
        )

    def update(self, plan: Plan) -> Optional[Plan]:
        try:
            record = PlanModel.get(PlanModel.id == plan.id)
            record.name = plan.name
            record.description = plan.description
            record.price = plan.price
            record.save()
            return Plan(
                id=record.id,
                name=record.name,
                description=record.description,
                price=record.price
            )
        except PlanModel.DoesNotExist:
            return None

    def delete(self, plan_id: int) -> bool:
        try:
            record = PlanModel.get(PlanModel.id == plan_id)
            record.delete_instance()
            return True
        except PlanModel.DoesNotExist:
            return False

