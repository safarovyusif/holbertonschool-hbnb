from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # Validasiya qaydaları
        if not email or "@" not in email:
            raise ValueError("Email is required and must be valid")
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be max 50 chars")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be max 50 chars")
