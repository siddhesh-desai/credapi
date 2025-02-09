import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException


load_dotenv()

app = FastAPI()

app.mongodb_client = MongoClient(os.getenv("ATLAS_URI"))
app.database = app.mongodb_client[os.getenv("DB_NAME")]


def convert_object_ids(doc):
    """Recursively convert ObjectId fields to strings in a document."""
    if isinstance(doc, dict):
        return {k: convert_object_ids(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_object_ids(i) for i in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc


@app.get("/get-user-info/{user_id}")
async def get_user_info(user_id: str):
    try:
        user_info = app.database["users"].find_one({"_id": ObjectId(user_id)})
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        # user_info["_id"] = str(user_info["_id"])
        return convert_object_ids(user_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
