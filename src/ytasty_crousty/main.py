from fastapi import FastAPI
from ytasty_crousty.modules.auths.router import router as auth_router

from ytasty_crousty.modules.restaurants.models import Restaurant  # noqa: F401
from ytasty_crousty.modules.users.models import User  # noqa: F401
from ytasty_crousty.modules.products.models import Product  # noqa: F401
from ytasty_crousty.modules.ordres.models import Order, OrderItem  # noqa: F401
 
app = FastAPI(title="Ytasty Crousty API")
app.include_router(auth_router)
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
