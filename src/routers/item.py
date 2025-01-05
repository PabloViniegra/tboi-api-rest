from fastapi import APIRouter, Depends, HTTPException
from src.schemas.schemas import ResponseItemSchema, ItemSchema, PatchItemSchema
from src.database.models.item import Item
from sqlalchemy.orm import Session
from src.database.db import get_db
from sqlalchemy import or_, asc, desc, nulls_last
from math import ceil
from fastapi import Query

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/", response_model=ResponseItemSchema)
def get_items(page: int = Query(1, ge=1), limit: int = Query(10, ge=1), q: str = None, sort: str = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of items with pagination based on pages and optional search query.

    Args:
        page (int, optional): The page number to retrieve. Defaults to 1.
        limit (int, optional): The number of items per page. Defaults to 10.
        q (str, optional): The search query to filter items. Defaults to None.
        sort (str, optional): The sort order of items. Defaults to None.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the total count, total pages, current page, and the list of items.
    """
    try:
        query = db.query(Item)

        if q:
            query = query.filter(
                or_(
                    Item.title.ilike(f"%{q}%"),
                    Item.short_description.ilike(f"%{q}%"),
                    Item.description.ilike(f"%{q}%")
                )
            )

        if sort:
            if sort == 'alphabetical-asc':
                query = query.order_by(asc(Item.title))
            elif sort == 'alphabetical-desc':
                query = query.order_by(desc(Item.title))
            elif sort == 'quality-asc':
                query = query.order_by(nulls_last(asc(Item.quality)))
            elif sort == 'quality-desc':
                query = query.order_by(nulls_last(desc(Item.quality)))

        total_items = query.count()
        skip = (page - 1) * limit
        items = query.offset(skip).limit(limit).all()
        serialized_items = [ItemSchema.model_validate(item) for item in items]
        total_pages = ceil(total_items / limit) if limit > 0 else 1

        response = {
            'count': total_items,
            'pages': total_pages,
            'page': page,
            'items': serialized_items
        }

        return response
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.get("/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an item by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.
        db (Session): The database session.

    Returns:
        ItemSchema: The retrieved item.

    Raises:
        HTTPException: If the item is not found or an error occurs.
    """
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.patch("/{item_id}", response_model=ItemSchema)
def patch_item(item_id: int, item: PatchItemSchema, db: Session = Depends(get_db)):
    """
    Update an item by its ID.

    Args:
        item_id (int): The ID of the item to update.
        item (PatchItemSchema): The item data to update.
        db (Session): The database session.

    Returns:
        ItemSchema: The updated item.

    Raises:
        HTTPException: If the item is not found or an error occurs.
    """
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item by its ID.

    Args:
        item_id (int): The ID of the item to delete.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message that the item was deleted successfully.
    Raises:
        HTTPException: If the item is not found or an error occurs.
    """
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")
