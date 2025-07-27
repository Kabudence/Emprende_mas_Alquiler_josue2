from enum import Enum


class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Subscription:
    def __init__(self,
                 id: int = None,
                 plan_id: int = None,
                 negocio_id: int = None,
                 initial_date: str = "",
                 final_date: str = "",
                 status: SubscriptionStatus = SubscriptionStatus.ACTIVE,
                 ):
        self.id = id
        if plan_id is None:
            raise ValueError("plan_id cannot be None")
        self.plan_id = plan_id
        if negocio_id is None:
            raise ValueError("negocio_id cannot be None")
        self.negocio_id = negocio_id
        if initial_date is None or initial_date.strip() == "":
            raise ValueError("initial_date cannot be None or empty")
        self.initial_date = initial_date
        if final_date is None or final_date.strip() == "":
            raise ValueError("final_date cannot be None or empty")
        self.final_date = final_date

        self.status = status
    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "negocio_id": self.negocio_id,
            "initial_date": self.initial_date,
            "final_date": self.final_date,
            "status": self.status
        }