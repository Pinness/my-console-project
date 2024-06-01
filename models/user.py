from models.base_model import BaseModel
from models import storage

class User(BaseModel):
    """User class inheriting from BaseModel"""

    def __init__(self, *args, **kwargs):
        """Initialise User attribute"""

        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')

