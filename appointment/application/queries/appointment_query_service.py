from datetime import date
from typing import List

from appointment.domain.entities.appointment import Appointment
from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository

class AppointmentQueryService:
    def __init__(self, appointment_repo: AppointmentRepository):
        self.appointment_repo = appointment_repo

    def get_by_id(self, appointment_id: int):
        return self.appointment_repo.get_by_id(appointment_id)

    def list_by_staff_and_day(self, staff_id: int, day: str):
        return self.appointment_repo.list_by_staff_and_day(staff_id, day)

    def list_future_by_negocio(self, negocio_id: int):
        return self.appointment_repo.get_by_negocio(negocio_id)

    def list_by_day_and_negocio(self, day: str, negocio_id: int) -> List[Appointment]:
        return self.appointment_repo.get_by_day_negocio_id(day, negocio_id)

        # NUEVO → todas las citas de un mes

    def list_by_month_and_negocio(self, *, year: int, month: int, negocio_id: int) -> List[Appointment]:
        first = date(year, month, 1).isoformat()  # '2025‑07‑01'
        if month == 12:
            last = date(year + 1, 1, 1).isoformat()  # exclusivo
        else:
            last = date(year, month + 1, 1).isoformat()
        return self.appointment_repo.list_between_dates(negocio_id, first, last)