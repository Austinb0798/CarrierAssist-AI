from fastapi import FastAPI, HTTPException

app = FastAPI()

customers = {
    "1001": {
        "customer_id": "1001",
        "name": "Alex Carter",
        "account_status": "active",
        "plan": "Unlimited Premium",
        "balance_due": 0.00,
        "device": "iPhone 17 Pro",
        "esim_status": "active",
        "line_status": "active",
        "zip_code": "32724",
        "upgrade_eligible": True
    },
    "1002": {
        "customer_id": "1002",
        "name": "Jordan Lee",
        "account_status": "active",
        "plan": "Unlimited Standard",
        "balance_due": 42.18,
        "device": "Galaxy S26 Ultra",
        "esim_status": "active",
        "line_status": "active",
        "zip_code": "32724",
        "upgrade_eligible": False
    },
    "1003": {
    "customer_id": "1003",
    "name": "Morgan Reed",
    "account_status": "active",
    "plan": "Unlimited Premium",
    "balance_due": 0.00,
    "device": "iPhone 16 Pro",
    "esim_status": "active",
    "line_status": "suspended",
    "zip_code": "32724",
    "upgrade_eligible": False
    },
    "1004": {
    "customer_id": "1004",
    "name": "Taylor Brooks",
    "account_status": "active",
    "plan": "Unlimited Standard",
    "balance_due": 0.00,
    "device": "Pixel 11 Pro",
    "esim_status": "inactive",
    "line_status": "active",
    "zip_code": "32724",
    "upgrade_eligible": True
    },
    "1005": {
    "customer_id": "1005",
    "name": "Casey Monroe",
    "account_status": "active",
    "plan": "Unlimited Premium",
    "balance_due": 0.00,
    "device": "Galaxy S26",
    "esim_status": "active",
    "line_status": "active",
    "zip_code": "32720",
    "upgrade_eligible": False
    },
    "1006": {
    "customer_id": "1006",
    "name": "Riley Shaw",
    "account_status": "inactive",
    "plan": "Unlimited Standard",
    "balance_due": 87.54,
    "device": "iPhone 17",
    "esim_status": "active",
    "line_status": "active",
    "zip_code": "32724",
    "upgrade_eligible": False
    },
    "1007": {
    "customer_id": "1007",
    "name": "Jamie Cole",
    "account_status": "active",
    "plan": "Unlimited Standard",
    "balance_due": 156.32,
    "device": "Galaxy S26 Ultra",
    "esim_status": "active",
    "line_status": "active",
    "zip_code": "32724",
    "upgrade_eligible": False
    },
}

outages = {
    "32720": {
        "outage": True,
        "service": "5G",
        "estimated_resolution": "2 hours"
    },
    "32724": {
        "outage": False,
        "service": "5G",
        "estimated_resolution": None
    }
}

@app.get("/")
def root():
    return {"message": "CarrrierAssist AI backend is running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CarrierAssist AI"
    }

@app.get("/customers")
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

@app.get("/customers/{customer_id}")
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

@app.get("/devices/{customer_id}")
def get_device_status(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "device": customer["device"],
        "esim_status": customer["esim_status"]
    }

@app.get("/lines/{customer_id}")
def get_line_status(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "line_status": customer["line_status"]
    }

@app.get("/upgrades/{customer_id}")
def check_upgrade_eligibility(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "upgrade_eligible": customer["upgrade_eligible"]
    }

@app.get("/billing/{customer_id}")
def get_billing(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "balance_due": customer["balance_due"]
    }

@app.get("/network/outages/{zip_code}")
def check_outage(zip_code: str):
    outage = outages.get(zip_code)

    if not outage:
        raise HTTPException(status_code=404, detail="ZIP code not found")

    return {
        "zip_code": zip_code,
        **outage
    }

@app.get("/troubleshoot/{customer_id}")
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

@app.post("/lines/{customer_id}/restore")
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

@app.post("/esim/{customer_id}/reactivate")
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

@app.get("/accounts/{customer_id}")
def get_account_status(customer_id: str):
    customer = customers.get(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer_id,
        "account_status": customer["account_status"]
    }