from sqlalchemy import select, update
from sqlalchemy.engine import Result, Row
from sqlalchemy.orm import Session

import api.models.mindmap as mindmap_model
import api.schemas.mindmap as mindmap_schema

def add_mindmap_item(db: Session,
        add_mindmap: mindmap_schema.AddDBMindMapItem,
        user_id: int) -> mindmap_model.Mindmap:
    mindmap_item = mindmap_model.Mindmap(**add_mindmap.dict(), user_id=user_id)
    db.add(mindmap_item)
    db.commit()
    db.refresh(mindmap_item)
    return mindmap_item

def get_multiple_mindmaps(
    db: Session,
) -> list[Row]:
    result: Result = db.execute(
        select(
            mindmap_model.Mindmap.id,
            mindmap_model.Mindmap.title,
            mindmap_model.Mindmap.nodes_json,
            mindmap_model.Mindmap.registration_date,
            mindmap_model.Mindmap.user_id,
            )
        )
    return result.all()

def get_mindmap(
    db: Session,
    mindmap_id: int,
) -> Row | None:
    result: Result = db.execute(
        select(
            mindmap_model.Mindmap.id,
            mindmap_model.Mindmap.title,
            mindmap_model.Mindmap.nodes_json,
            mindmap_model.Mindmap.registration_date,
            mindmap_model.Mindmap.user_id,
        )
        .filter(mindmap_model.Mindmap.id == mindmap_id)
    )
    return result.first()

# def update_mindmap_item(
#         db: Session, 
#         existing_mindmap: mindmap_model.Mindmap,
#         mindmap_update: mindmap_schema.MindMapBase
# ) -> mindmap_model.Mindmap:
#     update_data = mindmap_update.dict(exclude_unset=True)
#     db.execute(
#         update(mindmap_model.Mindmap.__table__)
#         .where(mindmap_model.Mindmap.id == existing_mindmap.id)
#         .values(update_data)
#     )
#     db.commit()
#     return existing_mindmap

def update_mindmap_item(db: Session, mindmap_id: int, update_data: dict) -> mindmap_model.Mindmap:
    db.execute(
        update(mindmap_model.Mindmap.__table__)
        .where(mindmap_model.Mindmap.id == mindmap_id)
        .values(update_data)
    )
    db.commit()
    return get_mindmap(db, mindmap_id)
