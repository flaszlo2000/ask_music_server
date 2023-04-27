from http import HTTPStatus
from typing import Optional

from fastapi import Body, FastAPI, HTTPException
from pydantic.dataclasses import dataclass
from pydantic.fields import Field

app = FastAPI()

@dataclass
class WebhooksCode():
    value1: Optional[str] = Field(default = None)
    value2: Optional[str] = Field(default = None)
    value3: Optional[str] = Field(default = None)

    def __post_init__(self):
        if not any((self.value1, self.value2, self.value3)):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Must have at least one value not null!")

@app.post("/")
async def code(code: WebhooksCode = Body(...)):
    print(code)
