from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas.schemas import PublisherCreate, PublisherRead, PublisherUpdate

from app.services.database import get_db
from app.resources import Tags
from app.models import Publisher


publishers_router = APIRouter(prefix='/publishers')


@publishers_router.post(
    '/', 
    response_model=PublisherRead, 
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.Publishers]
)
def create_publisher(*, db: Session = Depends(get_db), publisher: PublisherCreate):
    try:
        new_publisher = Publisher(name=publisher.name, description=publisher.description)
        db.add(new_publisher)
        db.commit()
        db.refresh(new_publisher)

        return new_publisher
    except IntegrityError:
        db.rollback()
        db.close()
        raise HTTPException(status_code=400, detail="Publisher already exists.")


@publishers_router.get(
    '/{publisher_id}', 
    response_model=PublisherRead, 
    response_model_exclude_none=True,
    tags=[Tags.Publishers]
)
def get_publisher_by_id(*, db: Session = Depends(get_db), publisher_id: int):
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()

    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found.")

    return publisher


@publishers_router.get(
    '/', 
    response_model=list[PublisherRead], 
    response_model_exclude_none=True,
    tags=[Tags.Publishers]
)
def get_all_publishers(
    *, db: Session = Depends(get_db), 
    name: str | None = Query(None, min_length=3, max_length=20)
):
    if name:
        return db.query(Publisher).filter(Publisher.name.ilike('%' + name + '%')).all()
    
    return db.query(Publisher).all()


@publishers_router.patch(
    '/{publisher_id}', 
    response_model=PublisherRead, 
    response_model_exclude_none=True,
    tags=[Tags.Publishers]
)
def update_publisher(*, db: Session = Depends(get_db), publisher_id: int, publisher: PublisherUpdate):
    db_publisher = db.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    
    publisher_data = publisher.dict(exclude_unset=True)
    for key, value in publisher_data.items():
            setattr(db_publisher, key, value)
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


@publishers_router.delete('/{publisher_id}', tags=[Tags.Publishers])
def delete_author(*, db: Session = Depends(get_db), publisher_id: int):
    publisher = db.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    
    db.delete(publisher)
    db.commit()
    return {'ok': True}
