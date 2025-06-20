from sqlalchemy.orm import Session
from app import models, schemas

def get_target(db: Session, target_id: int):
    return db.query(models.Target).filter(models.Target.id == target_id).first()

def update_target(db: Session, target_id: int, target_update: schemas.TargetUpdate):
    db_target = get_target(db, target_id)
    if db_target:
        update_data = target_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_target, key, value)
        
        mission = db_target.mission
        
        if mission and all(t.complete for t in mission.targets):
            mission.complete = True

        db.commit()
        db.refresh(db_target)
        
        if mission:
            db.refresh(mission)
    return db_target