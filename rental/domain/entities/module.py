class Module:
    def __init__(self,
                 id : int = None,
                 name: str = "",
                 description: str = "",
                 ):
        self.id = id
        self.name = name
        self.description = description
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }