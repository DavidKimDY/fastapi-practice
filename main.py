from enum import Enum
from typing import Optional, List
import datetime

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None,
    price: float = 10.0
    tax: Optional[float] = None


@app.post('/item/')
def post_item(item: Item):
    res = item.dict()
    return res


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


@app.get("/")
async def root():
    return {"Today": datetime.datetime.today().isoformat()}


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.lenet:
        return {'model_name': model_name}
    if model_name == ModelName.alexnet:
        return {'model_name': model_name}
    else:
        return {'model_name': 'Nothing'}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
       price_with_tax = item.price + item.tax
       item_dict['price_with_tax'] = price_with_tax
    return item_dict


@app.post("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [
    {"item_name": "foo"},
    {"item_name": "coco"},
    {"item_name": "hi man"}
]


@app.get("/items/{item_id}")
async def read_item(
        item_id: str = Path(
            ...,
            title="I don't know why title is settable",
        ),
        q: Optional[List[str]] = Query(
            ...,
            max_length=50,
            alias="item-query",
            title="*****",
            description="Query string for the items to search in the database that have a good match"
        ),
        short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update(
            {'description': 'This item has a long description'}
        )
    return item


class Coffee(str, Enum):
    hot = 'Hot'
    cold = 'Cold'


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, coffee: Coffee, q: Optional[str] = None, short: bool = False,
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'A long description'})
    return item

