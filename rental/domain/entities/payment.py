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
        if user_id is None:
            raise ValueError("user_id cannot be None")
        self.user_id = user_id
        if amount is None or amount < 0:
            raise ValueError("amount cannot be None or negative")
        self.amount = amount
        if created_at is None or created_at.strip() == "":
            raise ValueError("created_at cannot be None or empty")
        self.created_at = created_at
        if status is None:
            raise ValueError("status cannot be None")
        self.status = status


     def to_dict(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "amount": self.amount,
                "created_at": self.created_at,
                "status": self.status.value if isinstance(self.status, PaymentStatus) else self.status
            }
