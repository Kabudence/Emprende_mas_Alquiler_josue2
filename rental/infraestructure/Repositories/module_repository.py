from typing import Optional, List

from rental.domain.entities.module import Module
from rental.infraestructure.model.module_model import ModuleModel


class ModuleRepository:
    def get_by_id(self, id: int) -> Optional[Module]:
        try:
            record = ModuleModel.get(ModuleModel.id == id)
            return Module(
                id=record.id,
                name=record.name,
                description=record.description
            )
        except ModuleModel.DoesNotExist:
            return None

    def get_all(self) -> List[Module]:
        return [
            Module(
                id=rec.id,
                name=rec.name,
                description=rec.description
            )
            for rec in ModuleModel.select()
        ]

    def create(self, module: Module) -> Module:
        record = ModuleModel.create(
            name=module.name,
            description=module.description
        )
        return Module(
            id=record.id,
            name=record.name,
            description=record.description
        )

    def update(self, module: Module) -> Optional[Module]:
        try:
            record = ModuleModel.get(ModuleModel.id == module.id)
            record.name = module.name
            record.description = module.description
            record.save()
            return Module(
                id=record.id,
                name=record.name,
                description=record.description
            )
        except ModuleModel.DoesNotExist:
            return None

    def delete(self, module_id: int) -> bool:
        try:
            record = ModuleModel.get(ModuleModel.id == module_id)
            record.delete_instance()
            return True
        except ModuleModel.DoesNotExist:
            return False
