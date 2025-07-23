from datetime import datetime, timezone, timedelta

from peewee import fn
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # estándar en Python 3.9+

from appointment.domain.entities.appointment import Appointment, AppointmentStatus
from appointment.infraestructure.models.appointment_model import AppointmentModel


class AppointmentRepository:
    def get_by_day_negocio_id(self, day: str, negocio_id: int) -> list:
        """
        Retrieves appointments for a specific day (YYYY-MM-DD) and negocio_id.
        """
        query = AppointmentModel.select().where(
            (fn.DATE(AppointmentModel.start_time) == day) &
            (AppointmentModel.negocio_id == negocio_id)
        )
        return [self._from_model(record) for record in query]

    def get_by_negocio(self, negocio_id: int) -> list:
        """
        """
        now_pe = datetime.now(ZoneInfo("America/Lima"))
        query = AppointmentModel.select().where(
            (AppointmentModel.negocio_id == negocio_id) &
            (AppointmentModel.end_time >= now_pe)
        )
        return [self._from_model(record) for record in query]

    def list_by_staff_and_day(self, staff_id: int, day: str):
        from datetime import datetime
        from peewee import fn

        try:
            _date = datetime.strptime(day, "%Y-%m-%d")
            day_name = _date.strftime("%A")  # 'Monday', 'Tuesday', etc
        except ValueError:
            day_name = ES_TO_EN_DAYNAME.get(day, day)


        query = (
            AppointmentModel
            .select()
            .where(
                (fn.DAYNAME(AppointmentModel.start_time) == day_name) &
                (AppointmentModel.staff_id == staff_id) &
                (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
            )
        )
        print(f"[DEBUG-REPOSITORY LVL] SQL generado: {query.sql()}")

        preview_query = (
            AppointmentModel
            .select(
                AppointmentModel.id,
                AppointmentModel.start_time,
                fn.DAYNAME(AppointmentModel.start_time).alias('real_dayname'),
                AppointmentModel.status
            )
            .where(
                (AppointmentModel.staff_id == staff_id) &
                (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
            )
            .order_by(AppointmentModel.start_time)
            .limit(10)  # Puedes quitar el limit si quieres ver todos
        )

        print(f"[DEBUG-REPOSITORY LVL] Ejemplo de valores reales de DAYNAME(start_time) para staff_id={staff_id}:")
        for row in preview_query:
            print(
                f"ID: {row.id} | start_time: {row.start_time} | real DAYNAME: {row.real_dayname} | status: {row.status}")

        return query

    def is_staff_free(self,
                      staff_id: int,
                      start: datetime,
                      end: datetime) -> bool:
        """True si el staff no tiene ninguna cita que se superponga."""
        clash = (AppointmentModel
                 .select()
                 .where(
                     (AppointmentModel.staff_id == staff_id) &
                     (AppointmentModel.start_time < end) &
                     (AppointmentModel.end_time   > start) &   # intervalo abierto
                     (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
                 )
                 .exists())
        return not clash





    def _from_model(self, record) -> Appointment:
        # Convierte un AppointmentModel en Appointment
        return Appointment(
            id=record.id,
            start_time=record.start_time,
            end_time=record.end_time,
            client_id=record.client_id,
            negocio_id=record.negocio_id,
            staff_id=record.staff_id,
            status=AppointmentStatus(record.status),
            business_id=record.business_id,
            service_id=record.service_id,
        )

    def create(self, appointment: Appointment) -> Appointment:
        # Crea el registro en la base de datos
        record = AppointmentModel.create(
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            client_id=appointment.client_id,
            negocio_id=appointment.negocio_id,
            staff_id=appointment.staff_id,
            business_id=appointment.business_id,
            service_id=appointment.service_id,
            status=appointment.status.value if isinstance(appointment.status, AppointmentStatus) else appointment.status
        )
        # Devuelve el entity actualizado con el id real
        return self._from_model(record)

    def update(self, appointment: Appointment) -> Appointment:
        # Actualiza el registro existente
        query = AppointmentModel.update(
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            client_id=appointment.client_id,
            negocio_id=appointment.negocio_id,
            staff_id=appointment.staff_id,
            business_id=appointment.business_id,
            service_id=appointment.service_id,
            status=appointment.status.value if isinstance(appointment.status, AppointmentStatus) else appointment.status
        ).where(AppointmentModel.id == appointment.id)
        query.execute()
        # Recupera y retorna la versión actualizada
        return self.get_by_id(appointment.id)

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        try:
            record = AppointmentModel.get(AppointmentModel.id == appointment_id)
            return self._from_model(record)
        except AppointmentModel.DoesNotExist:
            return None

    # ------------------------------------------------------------------
    # NUEVO ➊  -  citas entre dos fechas ISO (inclusive/exclusivo)
    # ------------------------------------------------------------------
    def list_between_dates(self,
                           negocio_id: int,
                           date_from_iso: str,
                           date_to_iso: str) -> list:
        """
        Devuelve TODAS las citas cuyo start_time esté en el rango:
        [date_from_iso, date_to_iso)  (incluye inicio, excluye fin).

        • date_from_iso y date_to_iso deben venir como 'YYYY-MM-DD'.
        • Ignora citas CANCELLED.
        """
        from_date = self._iso_to_datetime(date_from_iso)
        to_date   = self._iso_to_datetime(date_to_iso)

        query = (AppointmentModel
                 .select()
                 .where(
                     (AppointmentModel.negocio_id == negocio_id) &
                     (AppointmentModel.start_time >= from_date) &
                     (AppointmentModel.start_time <  to_date) &
                     (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
                 ))
        print(f"Query: {query.sql()}")

        return [self._from_model(r) for r in query]

    # ------------------------------------------------------------------
    # Helper interno – convierte 'YYYY-MM-DD'  →  datetime 00:00:00
    # ------------------------------------------------------------------
    @staticmethod
    def _iso_to_datetime(iso_str: str) -> datetime:
        """'YYYY‑MM‑DD' → datetime 00:00:00 con tz Lima (o UTC‑5)."""
        tz_lima = _safe_zoneinfo("America/Lima")
        return datetime.strptime(iso_str, "%Y-%m-%d").replace(tzinfo=tz_lima)


    def get_last_pending_by_client(self, client_id: int) -> Appointment | None:
        """
        Devuelve la última (más reciente) cita con estado PENDING para un client_id.
        Si no hay, retorna None.
        """
        from appointment.domain.entities.appointment import AppointmentStatus  # asegúrate que está importado
        try:
            record = (
                AppointmentModel
                .select()
                .where(
                    (AppointmentModel.client_id == client_id) &
                    (AppointmentModel.status == AppointmentStatus.PENDING.value)
                )
                .order_by(AppointmentModel.start_time.desc())
                .get()
            )
            return self._from_model(record)
        except AppointmentModel.DoesNotExist:
         return None

def _safe_zoneinfo(key: str):
    """
    Devuelve ZoneInfo(key) o, si no existe, una tz fija UTC‑5 (Lima).
    """
    try:
        return ZoneInfo(key)
    except ZoneInfoNotFoundError:
        # UTC‑5 sin cambio horario
        return timezone(timedelta(hours=-5))
# ─────────────────────────────────────────────────────────────

ES_TO_EN_DAYNAME = {
    "Lunes": "Monday",
    "Martes": "Tuesday",
    "Miércoles": "Wednesday",
    "Jueves": "Thursday",
    "Viernes": "Friday",
    "Sábado": "Saturday",
    "Domingo": "Sunday"
}

