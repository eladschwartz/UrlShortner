from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .config import settings
from .routers.routers import ROUTERS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from .enums import Environment
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# Only want to limit when working vs PROD
if settings.ENVIRONMENT != Environment.DEVELOPMENT:
    limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)


print(settings.origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET, POST", "DELETE", "PUT"],
    allow_headers=["*"],
)

# Only want HTTPS when working vs PROD
if settings.ENVIRONMENT != Environment.DEVELOPMENT:
    app.add_middleware(HTTPSRedirectMiddleware)


for router in ROUTERS:
    app.include_router(router)