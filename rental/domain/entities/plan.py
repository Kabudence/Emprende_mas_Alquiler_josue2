class Plan:
    def __init__(self,
                 id: int= None,
                name :str = "",
                description: str = "",
                price: float = None,
                 ):
        self.id = id
        if name is None or name.strip() == "":
            raise ValueError("name cannot be none or empty")
        self.name = name
        if description is None or description.strip() == "":
            raise ValueError("description cannot be none or empty")
        self.description = description
        if price is None or price < 0:
            raise ValueError("price cannot be None or negative")
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }