from fastapi import APIRouter, HTTPException
from app.data.customers import customers

router = APIRouter()

@router.get("/lines/{customer_id}")
def get_line_status(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "line_status": customer["line_status"]
    }

@router.post("/lines/{customer_id}/restore")
def restore_line(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer["line_status"] != "suspended":
        return {
            "customer_id": customer_id,
            "message": "Line is not suspended",
            "line_status": customer["line_status"]
        }

    customer["line_status"] = "active"

    return {
        "customer_id": customer_id,
        "message": "Line restored successfully",
        "line_status": customer["line_status"]
    }