class Staff:
    def __init__(self,
                 id: int = None,
                 speciality: str = "",
                 name: str = "",
                 negocio_id: int = 0,
                 max_capacity: int = 0,
                 dni: str = ""
                 ):
        self.id = id
        self.speciality = speciality
        self.name = name
        self.negocio_id = negocio_id
        self.max_capacity = max_capacity
        self.dni = dni

    def __repr__(self):
        return (f"Staff(id={self.id}, speciality={self.speciality},"
                f" name={self.name}, business_id={self.negocio_id}, "
                f"max_capacity={self.max_capacity}, dni={self.dni})")

    def to_dict(self):
        """Convierte el objeto Staff a un diccionario."""
        return {
            "id": self.id,
            "speciality": self.speciality,
            "name": self.name,
            "negocio_id": self.negocio_id,
            "max_capacity": self.max_capacity,
            "dni": self.dni
        }
