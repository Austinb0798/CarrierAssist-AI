from fastapi import FastAPI
from app.routes.customers import router as customers_router
from app.routes.accounts import router as accounts_router
from app.routes.devices import router as devices_router
from app.routes.lines import router as lines_router
from app.routes.billing import router as billing_router
from app.routes.upgrades import router as upgrades_router
from app.routes.network import router as network_router
from app.routes.troubleshooting import router as troubleshooting_router

app = FastAPI()
app.include_router(customers_router)
app.include_router(accounts_router)
app.include_router(devices_router)
app.include_router(lines_router)
app.include_router(billing_router)
app.include_router(upgrades_router)
app.include_router(network_router)
app.include_router(troubleshooting_router)

@app.get("/")
def root():
    return {"message": "CarrrierAssist AI backend is running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CarrierAssist AI"
    }