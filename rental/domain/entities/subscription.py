class Subscription:
    def __init__(self,
                 id: int = None,
                 plan_id: int = None,
                 negocio_id: int = None,
                 initial_date: str = "",
                 final_date: str = "",
                 status: str = "active",
                 ):
        self.id = id
        self.plan_id = plan_id
        self.negocio_id = negocio_id
        self.initial_date = initial_date
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