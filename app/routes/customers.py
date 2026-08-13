from fastapi import APIRouter, HTTPException
from app.data.customers import customers

router = APIRouter()

@router.get("/customers")
def get_customers():
    return [
        {
            "customer_id": customer["customer_id"],
            "name": customer["name"],
            "plan": customer["plan"],
            "zip_code": customer["zip_code"]
        }
        for customer in customers.values()
    ]

@router.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer["customer_id"],
        "name": customer["name"],
        "plan": customer["plan"],
        "zip_code": customer["zip_code"]
    }