from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

# Crie o router
router = APIRouter()

def exposure_from_portfolio(portfolio: List[Dict[str, Any]]) -> float:
    """Return total notional exposure (sum qty * avg_price)"""
    total = 0.0
    for pos in portfolio:
        total += pos.get("quantity", 0) * pos.get("avg_price", 0.0)
    return total

def risk_level(exposure: float, account_size: float = 100000.0) -> str:
    ratio = exposure / account_size
    if ratio < 0.2:
        return "low"
    if ratio < 0.5:
        return "medium"
    return "high"

# Defina os endpoints
@router.get("/risk/exposure")
async def calculate_exposure(portfolio: List[Dict[str, Any]]):
    """Calculate total exposure from portfolio"""
    try:
        exposure = exposure_from_portfolio(portfolio)
        return {"exposure": exposure}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/risk/level")
async def get_risk_level(portfolio: List[Dict[str, Any]], account_size: float = 100000.0):
    """Get risk level based on portfolio exposure"""
    try:
        exposure = exposure_from_portfolio(portfolio)
        level = risk_level(exposure, account_size)
        return {
            "exposure": exposure,
            "account_size": account_size,
            "risk_level": level,
            "exposure_ratio": exposure / account_size
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/risk/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "risk"}