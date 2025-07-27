from enum import Enum


class PaymentStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class Payment:
     def __init__(self,
                  id : int = None,
                  user_id: int = None,
                  amount: float = 0.0,
                  created_at: str = "",
                  status: PaymentStatus = PaymentStatus.PENDING,
                  ):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.created_at = created_at
        self.status = status


     def to_dict(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "amount": self.amount,
                "created_at": self.created_at,
                "status": self.status.value if isinstance(self.status, PaymentStatus) else self.status
            }
