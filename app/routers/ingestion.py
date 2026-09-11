from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from typing import Any
from app.dependencies import get_current_user
from app.core.supabase_client import get_supabase
from app.schemas.readings import BiometricBatchRequest, BiometricBatchResponse

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

@router.post("/biometrics", response_model=BiometricBatchResponse)
async def ingest_biometrics(
    request: BiometricBatchRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: Client = Depends(get_supabase)
):
    if not request.readings:
        raise HTTPException(status_code=400, detail="Empty batch")
    
    user_id = current_user["id"]
    
    insert_data = []
    for reading in request.readings:
        data = reading.model_dump()
        data["user_id"] = user_id
        # Supabase API expects strings for datetime fields
        if data.get("recorded_at"):
            data["recorded_at"] = data["recorded_at"].isoformat()
        insert_data.append(data)
        
    try:
        response = db.table("biometric_readings").insert(insert_data).execute()
        
        inserted_rows = response.data
        inserted_count = len(inserted_rows)
        reading_ids = [row["id"] for row in inserted_rows]
        
        return BiometricBatchResponse(
            inserted_count=inserted_count,
            reading_ids=reading_ids
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
