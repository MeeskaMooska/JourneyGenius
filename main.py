# App
import os
from pymongo.mongo_client import MongoClient
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from test2 import fetch_map

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root
@app.get("/")
async def read_root(request: Request):
    airport_map = fetch_map()
    
    airport_map.get_root().render()
    map_header = airport_map.get_root().header.render()
    map_body_html = airport_map.get_root().html.render()
    map_script = airport_map.get_root().script.render()

    response_data = {
        'request': request,
        'map_header': map_header,
        'map_body_html': map_body_html,
        'map_script': map_script
    }

    return templates.TemplateResponse("index.html", response_data)