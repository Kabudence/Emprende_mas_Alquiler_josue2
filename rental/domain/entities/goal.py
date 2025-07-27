class Goal:
    def __init__ (self,
                  id : int = None,
                  number_of_clients: int = None,
                  month:int = None,
                  percentage_to_bonus: float = None,
                ):
        self.id = id
        if number_of_clients is None:
            raise ValueError("number_of_clients cannot be None")
        self.number_of_clients = number_of_clients
        if month is None:
            raise ValueError("month cannot be None")
        self.month = month
        if percentage_to_bonus is None:
            raise ValueError("percentage_to_bonus cannot be None")
        self.percentage_to_bonus = percentage_to_bonus

    def to_dict(self):
        return {
            "id": self.id,
            "number_of_clients": self.number_of_clients,
            "month": self.month,
            "percentage_to_bonus": self.percentage_to_bonus
        }