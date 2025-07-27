from typing import List, Optional
from rental.domain.entities.module import Module
from rental.infraestructure.Repositories.module_repository import ModuleRepository
from rental.infraestructure.model.module_model import ModuleModel

class ModuleQueryService:
    def __init__(self, module_repo: ModuleRepository):
        self.module_repo = module_repo

    def get_by_id(self, module_id: int) -> Optional[Module]:
        return self.module_repo.get_by_id(module_id)

    def list_all(self) -> List[Module]:
        return self.module_repo.get_all()

    def get_by_name(self, name: str) -> Optional[Module]:
        try:
            record = ModuleModel.get(ModuleModel.name == name)
            return Module(
                id=record.id,
                name=record.name,
                description=record.description
            )
        except ModuleModel.DoesNotExist:
            return None
