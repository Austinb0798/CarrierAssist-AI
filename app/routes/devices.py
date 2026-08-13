from fastapi import APIRouter, HTTPException
from app.data.customers import customers

router = APIRouter()

@router.get("/devices/{customer_id}")
def get_device_status(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "device": customer["device"],
        "esim_status": customer["esim_status"]
    }

@router.post("/esim/{customer_id}/reactivate")
def reactivate_esim(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer["esim_status"] == "active":
        return {
            "customer_id": customer_id,
            "message": "eSIM is already active",
            "esim_status": customer["esim_status"]
        }

    customer["esim_status"] = "active"

    return {
        "customer_id": customer_id,
        "message": "eSIM reactivated successfully",
        "esim_status": customer["esim_status"]
    }