from sqlalchemy.orm import Session
from app import models, schemas
from app.crud import get_cat

def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

def get_missions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mission).offset(skip).limit(limit).all()

def create_mission(db: Session, mission: schemas.MissionCreate):
    db_mission = models.Mission(complete=mission.complete)
    for target_data in mission.targets:
        db_target = models.Target(**target_data.model_dump())
        db_mission.targets.append(db_target)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission

def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    db_mission = get_mission(db, mission_id)
    db_cat = get_cat(db, cat_id)
    if db_mission and db_cat:
        db_mission.cat_id = cat_id
        db.commit()
        db.refresh(db_mission)
    return db_mission
    
def delete_mission(db: Session, mission_id: int):
    db_mission = get_mission(db, mission_id)
    if db_mission:
        db.delete(db_mission)
        db.commit()
    return db_mission