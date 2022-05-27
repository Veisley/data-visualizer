from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
from pandas import read_json
import io
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/sampleDataset/{name}",
    responses={
        404: {
            "description": "Not Found"
        },
        200: {
            "content": {
                "application/json": {}
            }
        }
    },
)
async def sampleDataset(name: str):

    try:
        data = sns.load_dataset(name)
    except:
        data = "data could not be loaded"

    return json.loads(data.to_json())


@app.get(
    "/sampleDatasetNames",
    responses={
        404: {
            "description": "Not Found"
        },
        200: {
            "content": {
                "application/json": {}
            }
        }
    },
)
async def getSampleDatasetNames():
    names = sns.get_dataset_names()
    return names


@app.get(
    "/graph/",
    responses={
        404: {
            "description": "Not Found"
        },
        200: {
            "content": {
                "image/png": {}
            }
        }
    },
)
async def graph(params: str):

    params = json.loads(params)
    options = params["options"]
    function = getattr(sns, options["plotType"])

    data = read_json(params["data"])
    fig = function(data=data, **options["args"])
    #sns.rugplot(data=data)

    with io.BytesIO() as figBytes:
        fig.savefig(figBytes, format="png")
        figBytes.seek(0)
        response = Response(figBytes.getvalue(), media_type="image/png")
        plt.close()

    return response
    
    #plt.close()
    #return HTMLResponse(mpld3.fig_to_html(fig.figure))
