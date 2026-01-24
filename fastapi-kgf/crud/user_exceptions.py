class UserBaseError(Exception):
    """Base exception CRUD actions"""


class UserAlreadyExists(UserBaseError):
    """Raised on short url creation if such slug already exists."""
