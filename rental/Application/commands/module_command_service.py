from rental.domain.entities.module import Module
from rental.infraestructure.Repositories.module_repository import ModuleRepository


class ModuleCommandService:
    def __init__(self, module_repo: ModuleRepository):
        self.module_repo = module_repo

    def create(self, name: str, description: str) -> Module:
        if not name or not description:
            raise ValueError("Missing required fields.")
        module = Module(name=name, description=description)
        return self.module_repo.create(module)

    def update(self, module_id: int, name: str, description: str) -> Module:
        module = self.module_repo.get_by_id(module_id)
        if not module:
            raise ValueError("Module not found")
        module.name = name
        module.description = description
        return self.module_repo.update(module)

    def delete(self, module_id: int) -> bool:
        return self.module_repo.delete(module_id)
