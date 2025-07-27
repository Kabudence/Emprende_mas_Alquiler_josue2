class CommissionsTypes:
    DIRECT = "direct"
    REFERRED = "referred"

class Commissions:
    def __init__(self,
                 id: int = None,
                 user_id: int = None,
                 subscription_id: int = None,
                 amount: float = None,
                 type :CommissionsTypes = CommissionsTypes.DIRECT,
                 created_at: str = "",
                 ):
        self.id = id
        if user_id is None:
            raise ValueError("user_id cannot be None")
        self.user_id = user_id

        self.subscription_id = subscription_id
        if amount is None:
            raise ValueError("amount cannot be None")
        self.amount = amount
        if type is None:
            raise ValueError("type cannot be None")
        self.type = type
        self.created_at = created_at
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subscription_id": self.subscription_id,
            "amount": self.amount,
            "type": self.type,
            "created_at": self.created_at
        }