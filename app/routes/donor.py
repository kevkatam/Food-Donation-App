from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


donors = {
    1: {
        "name": "kyalo",
        "age": "10",
        "id": 1
    },
    2: {
        "name": "kamau",
        "age": "20",
        "id": 2
    },
    3: {
        "name": "kamene",
        "age": "30",
        "id": 3
    }
}


class Donor(BaseModel):
    name: str
    age: int
    user_id: int


class UpdateDonor(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    id: Optional[int] = None


@app.get("/")
def index():
    return {"name": "First Data"}


"""path parameters"""


@app.get("/get-donor/{donor_id}")
def get_donor(donor_id: int = Path(..., description="The ID of the donor you want to view", gt=0)):
    return donors.get(donor_id, {"Data": "Not Found", "Status Code": 404})


"""query parameters"""


@app.get("/get-by-name")
def get_donor(*, donor_id: int, name: Optional[str] = None, test: int):
    for donor_id in donors:
        if donors[donor_id]["name"] == name:
            return donors[donor_id]
    return {"Data": "Not Found"}
    raise HTTPException(status_code=404, detail="Donor not found")


"""request body"""


@app.post("/create-donor/{donor_id}")
def create_donor(donor_id: int, donor: Donor):
    if donor_id in donors:
        return {"Error": "Donor ID already exists"}
    donors[donor_id] = donor
    return donors[donor_id]


@app.put("/update-donor/{donor_id}")
def update_donor(donor_id: int, donor: Donor):
    if donor_id not in donors:
        return {"Error": "Donor ID does not exist"}

    if donor.name is not None:
        donors[donor_id]["name"] = donor.name

    if donor.age is not None:
        donors[donor_id]["age"] = donor.age

    if donor.id is not None:
        donors[donor_id]["id"] = donor.id

    donors[donor_id] = donor
    return donors[donor_id]
    raise HTTPException(status_code=404, detail="Donor not found")


@app.delete("/delete-donor/{donor_id}")
def delete_donor(donor_id: int):
    if donor_id not in donors:
        return {"Error": "Donor ID does not exist"}
    del donors[donor_id]
    return {"Message": "Donor deleted successfully"}
