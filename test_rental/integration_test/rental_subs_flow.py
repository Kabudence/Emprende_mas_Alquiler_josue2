"""
integration_test.py
─────────────────────────────────────────────────────────────
• Inicializa las tablas Peewee (init_db)
• Crea repos, command‑ y query‑services
• Ejecuta el flujo seller / buyer con logs en consola
"""

# ──────────────── Dependencias principales ─────────────────
from init_db import app                 # tu objeto Flask
from shared.infrastructure.database import init_db

from app import db
from app.models import Usuario

# ────────── Repositorios (Peewee) ──────────────────────────
from rental.infraestructure.Repositories.goal_repository         import GoalRepository
from rental.infraestructure.Repositories.module_repository       import ModuleRepository
from rental.infraestructure.Repositories.plan_repository         import PlanRepository
from rental.infraestructure.Repositories.module_plan_repository  import PlanModuleRepository
from rental.infraestructure.Repositories.subscription_repository import SubscriptionRepository
from rental.infraestructure.Repositories.user_goal_repository    import UserGoalRepository
from rental.infraestructure.Repositories.commissions_repository  import CommissionRepository

# ────────── Command‑services ───────────────────────────────
from rental.Application.commands.goal_command_service         import GoalCommandService
from rental.Application.commands.module_command_service       import ModuleCommandService
from rental.Application.commands.plan_command_service         import PlanCommandService
from rental.Application.commands.subscription_command_service import SubscriptionCommandService
from rental.Application.commands.user_goal_command_service    import UserGoalCommandService
from rental.Application.commands.commissions_command_service  import CommissionCommandService

# ────────── Query‑services ─────────────────────────────────
from rental.Application.queries.plan_query_service            import PlanQueryService
from rental.Application.queries.commissions_query_service     import CommissionQueryService
from rental.Application.queries.user_goal_query_service       import UserGoalQueryService

# ────────── Servicio de flujo de negocio ───────────────────
from rental.Application.user_flow_service                     import UserFlowService


# ─────────────── Helpers de impresión ──────────────────────
def print_header(text: str) -> None:
    print("\n" + "=" * 12 + f" {text} " + "=" * 12)


# ─────────────── Crear repositorios ────────────────────────
goal_repo          = GoalRepository()
module_repo        = ModuleRepository()
plan_repo          = PlanRepository()
plan_module_repo   = PlanModuleRepository()
subscription_repo  = SubscriptionRepository()
user_goal_repo     = UserGoalRepository()
commission_repo    = CommissionRepository()

# ─────────────── Command‑services ──────────────────────────
goal_cmd          = GoalCommandService(goal_repo)
module_cmd        = ModuleCommandService(module_repo)
plan_cmd          = PlanCommandService(plan_repo, plan_module_repo)
subscription_cmd  = SubscriptionCommandService(subscription_repo)
user_goal_cmd     = UserGoalCommandService(user_goal_repo)
commission_cmd    = CommissionCommandService(commission_repo)

# ─────────────── Query‑services ────────────────────────────
plan_qry       = PlanQueryService(plan_repo)
commission_qry = CommissionQueryService(commission_repo)
user_goal_qry  = UserGoalQueryService(user_goal_repo)

# ─────────────── User‑flow service ─────────────────────────
user_flow_srv = UserFlowService(
    user_goal_cmd,
    subscription_cmd,
    commission_cmd,
    plan_qry
)

# ─────────────── Test de integración ───────────────────────
def test_user_flow():
    # 1) GOAL global
    print_header("Creando Goal global")
    goal = goal_cmd.create(10, 7, 0.30)
    print("Goal:", goal.to_dict())

    # 2) tres módulos + plan premium
    print_header("Creando módulos y plan premium")
    modules = [
        module_cmd.create(f"Módulo {i+1}", f"Funcionalidad {i+1}")
        for i in range(3)
    ]
    for m in modules:
        print("Módulo:", m.to_dict())

    plan = plan_cmd.create(
        "Plan Premium", "Plan con todo incluido", 100,
        ids_modules=[m.id for m in modules]
    )
    print("Plan:", plan.to_dict())

    # 3) dos afiliados
    print_header("Creando usuarios AFILIADO")
    u1 = Usuario(nombre="Afiliado 1", username="afiliado1",
                 email="af1@test.com", password="hashed",
                 id_tipo_usuario=1, dni="00000001", role="AFILIADO")
    db.session.add(u1); db.session.commit()

    u2 = Usuario(nombre="Afiliado 2", username="afiliado2",
                 email="af2@test.com", password="hashed",
                 id_tipo_usuario=1, dni="00000002",
                 role="AFILIADO", user_inviter=u1.id)
    db.session.add(u2); db.session.commit()

    user_flow_srv.seller_user_flow(u1.id)
    user_flow_srv.seller_user_flow(u2.id)
    print(f"Afiliados creados: {u1.id}, {u2.id}")

    # 4) 20 compradores
    print_header("Creando 20 COMPRADORES")
    compradores = []
    for i in range(20):
        invitador = u1 if i < 10 else u2
        comprador = Usuario(
            nombre=f"Comprador {i+1}", username=f"comprador{i+1}",
            email=f"comp{i+1}@test.com", password="hashed",
            id_tipo_usuario=2, dni=f"1000{i+1:03d}",
            role="COMPRADOR", user_inviter=invitador.id
        )
        db.session.add(comprador); db.session.commit()
        compradores.append(comprador)
    print("IDs:", [c.id for c in compradores])

    # 5) compras + comisiones
    print_header("Simulando compras / comisiones")
    acumulado = {u1.id: 0.0, u2.id: 0.0}
    for idx, comp in enumerate(compradores, 1):
        res = user_flow_srv.buyer_user_flow(comp.id, plan.id)
        print(f"Compra #{idx} – {comp.username}: S/ {res['commission'].amount:.2f}")

        afiliado = u1 if comp.user_inviter == u1.id else u2
        total = sum(c.amount for c in commission_qry.list_by_user_id(afiliado.id))
        acumulado[afiliado.id] = total

        goal_user = user_goal_qry.list_by_user(afiliado.id)[0]
        estado = "CUMPLIDA" if goal_user.goal_attained else "NO CUMPLIDA"
        print(f"   ↳ {afiliado.username}: total S/ {total:.2f} – meta {estado}")

    # 6) resumen
    print_header("RESUMEN FINAL")
    for uid, total in acumulado.items():
        print(f"Afiliado {uid} → TOTAL S/ {total:.2f}")


# ─────────────── Main ──────────────────────────────────────
if __name__ == "__main__":
    # 1. Crea (o verifica) las tablas Peewee
    init_db()

    # 2. Ejecuta dentro del contexto Flask
    with app.app_context():
        test_user_flow()
