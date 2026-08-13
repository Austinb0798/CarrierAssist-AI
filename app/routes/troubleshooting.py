from fastapi import APIRouter, HTTPException
from app.data.customers import customers
from app.data.outages import outages

router = APIRouter()

@router.get("/troubleshoot/{customer_id}")
def troubleshoot_customer(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer["account_status"] != "active":
        return {
        "customer_id": customer_id,
        "issue": "account_inactive",
        "recommended_action": "Review account status before continuing troubleshooting"
    }

    if customer["line_status"] == "suspended":
        return {
            "customer_id": customer_id,
            "issue": "line_suspended",
            "recommended_action": "Review account and restore line service"
        }

    if customer["esim_status"] == "inactive":
        return {
            "customer_id": customer_id,
            "issue": "esim_inactive",
            "recommended_action": "Reprovision or reactivate eSIM"
        }

    outage = outages.get(customer["zip_code"])

    if outage and outage["outage"]:
        return {
            "customer_id": customer_id,
            "issue": "network_outage",
            "recommended_action": "Wait for network restoration",
            "estimated_resolution": outage["estimated_resolution"]
        }

    return {
        "customer_id": customer_id,
        "issue": "no_known_issue",
        "recommended_action": "Continue device troubleshooting"
    }