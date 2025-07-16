import calendar
from datetime import date
from typing import Optional, List

from schedules.domain.entities.schedule import Schedule
from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository


class ScheduleQueryService:

    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository


    def get_by_negocio_business_and_day(self, negocio_id: int, business_id: int, day: str) -> Schedule:
            schedule = self.schedule_repository.get_by_day_and_business_and_negocio(day=day, business_id=business_id,
                                                                                    negocio_id=negocio_id)
            if not schedule:
                raise ValueError(f"No schedule found for day {day}, business {business_id} and negocio {negocio_id}.")
            return schedule

    def get_schedule_with_staff_by_negocio_business_and_day(
            self,
            negocio_id: int,
            business_id: Optional[int] = None,
            day: Optional[str] = None
    ):
        result = self.schedule_repository.get_schedule_with_staff(
            negocio_id=negocio_id,
            business_id=business_id,
            day=day
        )
        if not result or len(result) == 0:
            raise ValueError(
                f"No schedule+staff found for params: negocio_id={negocio_id}, business_id={business_id}, day={day}."
            )
        return result

    def get_all_days_by_negocio_business(self, negocio_id: int, business_id: Optional[int] = None) -> List[Schedule]:
        """
        Retrieve all days with schedules for a specific negocio and business.

        :param negocio_id: The ID of the negocio.
        :param business_id: The ID of the business.
        :return: List of days with schedules.
        """
        return self.schedule_repository.get_by_negocio_and_businessl(negocio_id=negocio_id, business_id=business_id)


    def get_by_id(self, horario_id):
        return self.schedule_repository.get_by_id(horario_id)

    def get_staff_by_schedule_query(self, schedule_id: int):
        return self.schedule_repository.get_staff_ids_by_schedulee(schedule_id)

    def get_days_with_schedule(self, *, negocio_id: int, year: int, month: int) -> List[int]:
        # 1. Schedules únicos por día‑semana (“Lunes”, …)
        schedules = self.get_all_days_by_negocio_business(negocio_id)
        days_of_week_scheduled = {s.day for s in schedules}

        # 2. Mapa ES ⇄ weekday()
        weekday_es_to_num = {
            "Lunes": 0, "Martes": 1, "Miércoles": 2, "Miercoles": 2,
            "Jueves": 3, "Viernes": 4,
            "Sábado": 5, "Sabado": 5,
            "Domingo": 6,
        }

        # 3. Recorre todos los días del mes y marca los que coinciden
        last_day = calendar.monthrange(year, month)[1]
        result = []
        for d in range(1, last_day + 1):
            dt = date(year, month, d)
            if any(dt.weekday() == weekday_es_to_num[nombre]
                   for nombre in days_of_week_scheduled):
                result.append(d)
        return result

    # -------------------------------------------------------------------------
    #  ➜  Lista de schedules para una fecha concreta  (detalle)
    # -------------------------------------------------------------------------
    def list_by_date_and_negocio(self, *, year: int, month: int, day: int, negocio_id: int) -> List[Schedule]:
        weekday_num_to_es = {
            0: "Lunes", 1: "Martes", 2: "Miércoles",
            3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo",
        }
        dia_semana = weekday_num_to_es[date(year, month, day).weekday()]
        # Filtra aquí, así no traes todo:
        return [s for s in self.get_all_by_negocio(negocio_id) if s.day == dia_semana]
