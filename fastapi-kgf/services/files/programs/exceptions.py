class ProgramBaseError(Exception):
    """Base exception CRUD actions"""


class ProgramFileNameAlreadyExistsError(ProgramBaseError):
    """Raised on program creation if file name already exists"""


class ProgramNameAlreadyExistsError(ProgramBaseError):
    """Raised on program creation if name already exists"""


class ProgramNameDoesNotExistError(ProgramBaseError):
    """Raised on program if name does not exist"""
