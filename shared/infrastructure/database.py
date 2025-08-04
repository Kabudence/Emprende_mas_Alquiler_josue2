"""
Database initialization module for the Smart Band Edge Service.
"""
from peewee import MySQLDatabase
from shared.infrastructure.db_config import DB_CONFIG

# Initialize the database connection
db = MySQLDatabase(**DB_CONFIG)

def init_db() -> None:
    """
    Initialize the database connection and create the necessary tables if they do not exist.
    """
    if db.is_closed():
        db.connect()
        print("Driver usado:", type(db._state.conn))

    # Import models here to avoid circular imports
    # Import models here to avoid circular imports
    from staff.infraestructure.models.staff_model import StaffModel
    from appointment.infraestructure.models.appointment_model import AppointmentModel
    from schedules.infraestructure.models.schedule_model import ScheduleModel, ScheduleStaffModel
    from rental.infraestructure.model.commissions_model import CommissionModel
    from rental.infraestructure.model.goal_model import GoalModel
    from rental.infraestructure.model.module_model import ModuleModel
    from rental.infraestructure.model.plan_model import PlanModel, PlanModuleModel
    from rental.infraestructure.model.subscription_model import SubscriptionModel
    from rental.infraestructure.model.user_goal_model import UserGoalModel

    db.create_tables([
        StaffModel, ScheduleModel, ScheduleStaffModel, AppointmentModel,
        GoalModel, ModuleModel, PlanModuleModel, PlanModel,
        SubscriptionModel, UserGoalModel, CommissionModel
    ], safe=True)

# shared/infrastructure/database.py
...
def init_db():
    if db.is_closed():
        db.connect()
    # Siempre imprime el driver
    print("Driver usado:", type(db._state.conn))
    ...


if __name__ == "__main__":
    init_db()
    # Mostrar estado explícitamente
    print("¿db está abierta? ->", not db.is_closed())
    print("Tablas existentes:", db.get_tables())
