from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.resources import Tags
from app.schemas.schemas import CategoryCreate, CategoryRead, CategoryUpdate

from app.auth.oauth2 import oauth2_scheme
from app.services.database import get_db
from app.models import Category


categories_router = APIRouter(prefix='/categories')


@categories_router.post(
    '/', 
    response_model=CategoryRead, 
    response_model_exclude_none=True, 
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.Categories],
    dependencies=[Depends(oauth2_scheme)]
)
def create_category(*, db: Session = Depends(get_db), category: CategoryCreate):
    try:
        new_category = Category(name=category.name, description=category.description)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category
    except IntegrityError:
        db.rollback()
        db.close()
        raise HTTPException(status_code=400, detail="Category already exists.")


@categories_router.get(
    '/{category_id}', 
    response_model=CategoryRead, 
    response_model_exclude_none=True,
    tags=[Tags.Categories]
)
def get_category_by_id(*, db: Session = Depends(get_db), category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    return category


@categories_router.get(
    '/', 
    response_model=list[CategoryRead], 
    response_model_exclude_none=True,
    tags=[Tags.Categories]
)
def get_all_categories(
    *, 
    db: Session = Depends(get_db), 
    name: str | None = Query(None, min_length=3, max_length=20)
):
    if name:
        return db.query(Category).filter(Category.name.ilike('%' + name + '%')).order_by(Category.id).all()
    
    return db.query(Category).all()


@categories_router.patch(
    '/{category_id}', 
    response_model=CategoryRead, 
    response_model_exclude_none=True,
    tags=[Tags.Categories],
    dependencies=[Depends(oauth2_scheme)]
)
def update_category(*, db: Session = Depends(get_db), category_id: int, category: CategoryUpdate):
    db_category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_data = category.dict(exclude_unset=True)
    for key, value in category_data.items():
            setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@categories_router.delete('/{category_id}', tags=[Tags.Categories], dependencies=[Depends(oauth2_scheme)])
def delete_author(*, db: Session = Depends(get_db), category_id: int):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {'ok': True}
