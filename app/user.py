
class User:
    """A base class for all users in the system."""
    def __init__(self, user_id, name, password):
    #initialize a new user
        self.id = user_id           #store user id
        self.name = name            #store user name
        self.password = password    #store user password