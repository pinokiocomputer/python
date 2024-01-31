from fastapi import FastAPI, Body
from typing import List
from pydantic import BaseModel
import sys
import os

import importlib
class Params(BaseModel):
  values: List[str]

app = FastAPI()
#@app.get("/")
#async def root():
# return {"greeting":"Hello world"}

 # { name: "pip.py", method: "list", params: [ ] }
@app.post("/call")
async def call(item: dict = Body(...)):
  print(f"item={item}")
  sys.path.insert(0, os.path.dirname(item["path"]))
#async def call(path: str, method: str, params: Params):
  mod = importlib.import_module(item["name"], item["path"])
  print(f"Mod = {mod}")
  fun = getattr(mod, item["method"])
  print(f"Fun = {fun}")
  result = fun(*item["params"])
  return result
