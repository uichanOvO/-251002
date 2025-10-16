from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB: dict[int, dict] = {}

class Item(BaseModel):
    name: str
    price: float

# CREATE
@app.post("/items", status_code=201)
async def create_item(item: Item):
    new_id = len(DB) + 1
    DB[new_id] = {"id" : new_id, **item.model_dump()}
    return {"id": new_id}

# READ
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(404, "not found")
    return DB[item_id]
# UPDATE
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in DB:
        raise HTTPException(404, "not found")
    DB[item_id].update(item.model_dump())
    return DB[item_id]

# DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(404, "not found")
    deleted = DB.pop(item_id)
    return {"deleted": deleted}