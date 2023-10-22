from pydantic import BaseModel, Field, root_validator

import typing


class AppResources(BaseModel):
    memory: str
    cpu: str
    gpu: str
    disk: str


class ChangeSet(BaseModel):
    app: str
    type: str
    pin_date: str
    resources: typing.List[AppResources] = Field(default_factor=list)
    metadata: typing.Optional[dict] = Field(default_factory=dict)
