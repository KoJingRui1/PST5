from app.user import User

class AdminUser(User):
    """Represents an admin, inheriting from the base User class."""
    def __init__(self, user_id, name, password):
        #Save as an user
        super().__init__(user_id, name, password)


        
