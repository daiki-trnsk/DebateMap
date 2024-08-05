
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from fastapi.logger import logger
import api.cruds.mindmap as mindmap_crud
import api.schemas.mindmap as mindmap_schema
from api.db import get_db
from api.extra_modules.auth.core import get_current_user
from api.extra_modules.image.core import save_image
from api.models.user import User as UserModel

router = APIRouter()

@router.post("/mindmap",response_model=mindmap_schema.AddMindMapResponse)
def add_mindmap(
    mindmap_api_body: mindmap_schema.AddMindMapItem,
    db:Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    ):
    mindmap_db_body = mindmap_schema.AddDBMindMapItem(
        title=mindmap_api_body.title,
        nodes_json = {
            "id": "root",
            "topic": mindmap_api_body.root_node_topic,
            "expanded": True,
            "children": [],
        },
    )
    return mindmap_crud.add_mindmap_item(db, mindmap_db_body, current_user.id)

@router.get("/mindmaps_list", response_model=list[mindmap_schema.MindMapItem])
def all_mindmap_list(
    db: Session = Depends(get_db),
):
    return mindmap_crud.get_multiple_mindmaps(db)

@router.get("/mindmap/{mindmap_id}", response_model=mindmap_schema.MindMapItem)
def get_mindmap(
    mindmap_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    mindmap = mindmap_crud.get_mindmap(db, mindmap_id=mindmap_id)
    if mindmap is None:
        raise HTTPException(status_code=404, detail="MindMap not found")
    
    return mindmap

@router.put("/mindmap/{mindmap_id}", response_model=mindmap_schema.MindMapItem)
def update_mindmap(
    mindmap_id: int,
    mindmap_update: mindmap_schema.MindMapBase,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    existing_mindmap = mindmap_crud.get_mindmap(db, mindmap_id=mindmap_id)
    if existing_mindmap is None:
        raise HTTPException(status_code=404, detail="MindMap not found")
    
    update_data = mindmap_update.dict(exclude_unset=True)
    updated_mindmap = mindmap_crud.update_mindmap_item(db, mindmap_id, update_data)

    return updated_mindmap
