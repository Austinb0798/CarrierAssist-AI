from fastapi import APIRouter, HTTPException
from app.data.outages import outages

router = APIRouter()

@router.get("/network/outages/{zip_code}")
def check_outage(zip_code: str):
    outage = outages.get(zip_code)

    if not outage:
        raise HTTPException(status_code=404, detail="ZIP code not found")

    return {
        "zip_code": zip_code,
        **outage
    }