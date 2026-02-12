from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR
from dependencies.session_auth import get_authenticated_user

templates = Jinja2Templates(directory=BASE_DIR / "templates")

templates.env.globals[get_authenticated_user.__name__] = get_authenticated_user
