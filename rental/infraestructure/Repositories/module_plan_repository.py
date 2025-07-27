from typing import List, Optional

from rental.infraestructure.model.plan_model import PlanModuleModel


class PlanModuleRepository:
    def add_module_to_plan(self, plan_id: int, module_id: int) -> bool:
        try:
            PlanModuleModel.create(plan_id=plan_id, module_id=module_id)
            return True
        except Exception:
            # Ya existe, o error DB
            return False

    def remove_module_from_plan(self, plan_id: int, module_id: int) -> bool:
        try:
            record = PlanModuleModel.get(
                (PlanModuleModel.plan_id == plan_id) &
                (PlanModuleModel.module_id == module_id)
            )
            record.delete_instance()
            return True
        except PlanModuleModel.DoesNotExist:
            return False

    def get_modules_by_plan(self, plan_id: int) -> List[int]:
        return [rec.module_id for rec in PlanModuleModel.select().where(PlanModuleModel.plan_id == plan_id)]

    def get_plans_by_module(self, module_id: int) -> List[int]:
        return [rec.plan_id for rec in PlanModuleModel.select().where(PlanModuleModel.module_id == module_id)]

    def exists(self, plan_id: int, module_id: int) -> bool:
        return PlanModuleModel.select().where(
            (PlanModuleModel.plan_id == plan_id) &
            (PlanModuleModel.module_id == module_id)
        ).exists()

    def remove_all_modules_from_plan(self, plan_id: int) -> int:
        """
        Elimina todas las relaciones de módulos para un plan dado.
        Devuelve el número de registros eliminados.
        """
        query = PlanModuleModel.delete().where(PlanModuleModel.plan_id == plan_id)
        rows_deleted = query.execute()
        return rows_deleted