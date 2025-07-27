from rental.domain.entities.plan import Plan
from rental.infraestructure.Repositories.module_plan_repository import PlanModuleRepository
from rental.infraestructure.Repositories.plan_repository import PlanRepository


class PlanCommandService:
    def __init__(self, plan_repo: PlanRepository, plan_module_repo: PlanModuleRepository):
        self.plan_repo = plan_repo
        self.plan_module_repo = plan_module_repo


    def create(self, name: str, description: str, price: float, ids_modules: list[int]) -> Plan:
        if not name or not description or price is None:
            raise ValueError("Missing required fields.")
        if price < 0:
            raise ValueError("Price must be non-negative.")
        if not isinstance(ids_modules, list):
            raise ValueError("ids_modules must be a list of module IDs.")

        plan = Plan(name=name, description=description, price=price)
        plan = self.plan_repo.create(plan)

        # Relacionar el plan con los módulos en la tabla intermedia
        for module_id in ids_modules:
            self.plan_module_repo.add_module_to_plan(plan.id, module_id)

        return plan

    def update(self, plan_id: int, name: str, description: str, price: float, ids_modules: list[int] = None) -> Plan:
        plan = self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found")
        plan.name = name
        plan.description = description
        plan.price = price
        updated_plan = self.plan_repo.update(plan)

        if ids_modules is not None:
            self.plan_module_repo.remove_all_modules_from_plan(plan_id)
            for module_id in ids_modules:
                self.plan_module_repo.add_module_to_plan(plan_id, module_id)

        return updated_plan

    def delete(self, plan_id: int) -> bool:
        return self.plan_repo.delete(plan_id)



