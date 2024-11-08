from fastapi import FastAPI, Response, Path, HTTPException, status
from pydantic import BaseModel
from utils.utils_random import random_alphanum
from service.short_link_service import ShortLinkService
import validators

short_link_service = ShortLinkService()
app = FastAPI()

@app.get("/health")
def health() -> str:
    return "ok"

class PutLink(BaseModel):
    link: str

@app.put("/link")
def put_link(long_link: PutLink) -> PutLink:
    if "https://" not in long_link.link:
        long_link.link="https://"+long_link.link
    if (validators.url(long_link.link)):
        short_link = short_link_service.put_link(long_link=long_link.link)
        return PutLink(link=f"http://localhost:8080/short/{short_link}")
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail="incorrect link")
    

@app.get("/short/{short_link}")
def get_link(short_link: str = Path(...)) -> Response:
    long_link = short_link_service.get_link(short_link=short_link)
    if long_link == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail="Link doesnt find")
    return Response(content=None, status_code=301, headers={"Location": long_link})


