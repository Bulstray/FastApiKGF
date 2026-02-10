from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR

from misc.auth import is_authenticated

templates = Jinja2Templates(directory=BASE_DIR / "templates")

templates.env.globals[is_authenticated.__name__] = is_authenticated
