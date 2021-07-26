from enum import Enum
from typing import Optional
import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None,
    price: float
    tax: Optional[float] = None


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
async def creat_item(item: Item):
    item_dict = item.dict()
    if item.tax:
       price_with_tax = item.price + item.tax
       item_dict['price_with_tax'] = price_with_tax
    return item_dict


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id" : item_id}
