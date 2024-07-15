import json
import requests

from fastapi.responses import Response
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request

with open('Api Responses/userabout.json', 'r') as json_file:
    about = json.loads(json_file.read())

with open('Api Responses/userinfo.json', 'r') as json_file:
    info = json.loads(json_file.read())

with open('Api Responses/usermedia.json', 'r') as json_file:
    media = json.loads(json_file.read())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/proxy")
async def proxy(request: Request):
    try:
        body = await request.json()
        url = body.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        response = requests.get(url)
        if response.status_code == 200:
            return Response(content=response.content, media_type=response.headers['Content-Type'])
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/proxy")
async def proxy(request: Request):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    try:
        body = await request.json()
        url = body.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        response = requests.get(url, headers)
        if response.status_code == 200:
            return Response(content=response.content, media_type=response.headers['Content-Type'])
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/about')
def get_about():
    return about


@app.get('/info')
def get_info():
    return info


@app.get('/media')
def get_media():
    return media


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
