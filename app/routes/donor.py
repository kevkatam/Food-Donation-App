from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

app = FastAPI()


# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["your_database_name"]
donors_collection = db["donors"]


class Donor(BaseModel):
    name: str
    age: int
    user_id: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateDonor(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    user_id: Optional[int] = None


def donor_helper(donor) -> dict:
    return {
        "id": str(donor["_id"]),
        "name": donor["name"],
        "age": donor["age"],
        "user_id": donor["user_id"],
    }


@app.get("/")
async def index():
    donors = []
    async for donor in donors_collection.find():
        donors.append(donor_helper(donor))
    return {"donors": donors}


@app.get("/get-donor/{donor_id}")
async def get_donor(donor_id: str):
    donor = await donors_collection.find_one({"_id": ObjectId(donor_id)})
    if donor:
        return donor_helper(donor)
    return {"Data": "Not Found"}


@app.post("/create-donor")
async def create_donor(donor: Donor):
    donor_dict = donor.dict()
    result = await donors_collection.insert_one(donor_dict)
    created_donor = await donors_collection.find_one({
        "_id": result.inserted_id})
    return donor_helper(created_donor)


@app.put("/update-donor/{donor_id}")
async def update_donor(donor_id: str, donor: UpdateDonor):
    donor_dict = donor.dict(exclude_unset=True)
    result = await donors_collection.update_one({
        "_id": ObjectId(donor_id)}, {"$set": donor_dict})
    if result.modified_count == 1:
        updated_donor = await donors_collection.find_one({
            "_id": ObjectId(donor_id)})
        return donor_helper(updated_donor)
    return {"Error": "Donor ID does not exist"}


@app.delete("/delete-donor/{donor_id}")
async def delete_donor(donor_id: str):
    result = await donors_collection.delete_one({"_id": ObjectId(donor_id)})
    if result.deleted_count == 1:
        return {"Message": "Donor deleted successfully"}
    return {"Error": "Donor ID does not exist"}
