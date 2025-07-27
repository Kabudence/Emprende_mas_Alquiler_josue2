class UserGoal:
    def __init__(self,
                 id : int = None,
                 user_id: int = None,
                 goal_id: int = None,
                    goal_attained: bool = False,
                 initial_date: str = "",
                 ):
        self.id = id
        if user_id is None:
            raise ValueError("user_id cannot be None")
        self.user_id = user_id
        if goal_id is None:
            raise ValueError("goal_id cannot be None")
        self.goal_id = goal_id
        self.goal_attained =  goal_attained
        self.initial_date = initial_date

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "goal_id": self.goal_id,
            "goal_attained": self.goal_attained,
            "initial_date": self.initial_date
        }