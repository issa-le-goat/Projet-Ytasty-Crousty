from fastapi import FastAPI, status

# Importation de tous les routeurs de l'application
from ytasty_crousty.modules.auths.router import router as auth_router
from ytasty_crousty.modules.users.router import router as users_router
from ytasty_crousty.modules.restaurants.router import router as restaurants_router
from ytasty_crousty.modules.products.router import router as products_router
from ytasty_crousty.modules.ordres.router import router as orders_router

app = FastAPI(
    title="Ytasty Crousty API",
    description="API REST pour la gestion du réseau de restaurants Ytasty Crousty.",
    version="1.0.0"
)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
def health_check():
    return {"status": "ok"}

# Enregistrement des différents modules (Routes)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(restaurants_router)
app.include_router(products_router)
app.include_router(orders_router)