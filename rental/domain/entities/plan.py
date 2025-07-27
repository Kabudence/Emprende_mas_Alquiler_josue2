class Plan:
    def __init__(self,
                 id: int= None,
                name :str = "",
                description: str = "",
                price: float = 0.0,
                 ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }