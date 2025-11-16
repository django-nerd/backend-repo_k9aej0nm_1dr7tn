import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import CallLog

app = FastAPI(title="Engineer Caller Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Engineer Caller Dashboard API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ----- Caller Logs Endpoints -----

class CallLogCreate(BaseModel):
    caller_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    category: CallLog.model_fields["category"].annotation  # reuse Literal
    subject: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = "ai-receptionist"
    assigned_to: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "new"

@app.post("/api/calls")
async def create_call(log: CallLogCreate):
    try:
        call_data = CallLog(**log.model_dump())
        inserted_id = create_document("calllog", call_data)
        return {"id": inserted_id, "message": "Call logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calls")
async def list_calls(category: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {"category": category} if category else {}
        docs = get_documents("calllog", filter_dict=filter_dict, limit=limit)
        # Convert ObjectId and datetime to string for JSON
        def serialize(d):
            d = dict(d)
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
            return d
        return [serialize(doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
