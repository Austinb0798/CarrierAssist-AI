from fastapi import APIRouter, HTTPException
from app.data.customers import customers

router = APIRouter()

@router.get("/billing/{customer_id}")
def get_billing(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "balance_due": customer["balance_due"]
    }