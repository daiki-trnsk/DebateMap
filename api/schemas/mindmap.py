import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import api.schemas.user as user_schema

class MindMapBase(BaseModel):
    title: str = Field(Sample="mindmapのタイトルA")
    nodes_json: Dict[str, Any]

class MindMapItem(MindMapBase):
    id: int
    user_id = int
    registration_date: datetime.datetime

    class Config:
        orm_mode = True

class AddMindMapItem(BaseModel):
    title: str = Field(Sample="記事タイトルA")
    root_node_topic: str = Field(Sample="議題を入力")

class AddDBMindMapItem(MindMapBase):
    pass

class AddMindMapResponse(MindMapBase):
    id: int
    registration_date: datetime.datetime
    # user: user_schema.UserResponse

    class Config:
        orm_mode = True
