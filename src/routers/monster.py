from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models.monster import Monster
from src.schemas.schemas import ResponseMonsterSchema, MonsterSchema, PlainMonsterSchema
from sqlalchemy import or_
from fastapi import Query
from math import ceil

router = APIRouter(
    prefix="/monsters",
    tags=["monsters"]
)


@router.get('/', response_model=ResponseMonsterSchema)
def get_monsters(page: int = Query(1, ge=1), limit: int = Query(10, ge=1), q: str = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of monsters with pagination based on pages and optional search query.

    Args:
        page (int, optional): The page number to retrieve. Defaults to 1.
        limit (int, optional): The number of monsters per page. Defaults to 10.
        q (str, optional): The search query to filter monsters. Defaults to None.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the total count, total pages, current page, and the list of monsters.
    """
    try:
        query = db.query(Monster)

        if q:
            query = query.filter(
                or_(
                    Monster.name.ilike(f"%{q}%"),
                    Monster.description.ilike(f"%{q}%")
                )
            )

        total_monsters = query.count()
        skip = (page - 1) * limit
        monsters = query.offset(skip).limit(limit).all()
        serialized_monsters = [MonsterSchema.model_validate(
            monster) for monster in monsters]
        total_pages = ceil(total_monsters / limit) if limit > 0 else 1

        response = {
            'count': total_monsters,
            'pages': total_pages,
            'page': page,
            'monsters': serialized_monsters
        }

        return response

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.get('/{monster_id}', response_model=MonsterSchema)
def get_monster(monster_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single monster based on the monster ID.

    Args:
        monster_id (int): The monster ID.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the monster details.
    """
    try:
        monster = db.query(Monster).filter(Monster.id == monster_id).first()

        if not monster:
            raise HTTPException(status_code=404, detail="Monster not found")

        return MonsterSchema.model_validate(monster)

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.post('/', response_model=MonsterSchema)
def create_monster(monster: PlainMonsterSchema, db: Session = Depends(get_db)):
    """
    Create a new monster based on the provided monster details.

    Args:
        monster (PlainMonsterSchema): The monster details.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the created monster details.

    """
    try:
        new_monster = Monster(
            name=monster.name,
            description=monster.description,
            image=monster.image
        )

        db.add(new_monster)
        db.commit()

        return MonsterSchema.model_validate(new_monster)

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.patch('/{monster_id}', response_model=MonsterSchema)
def update_monster(monster_id: int, monster: PlainMonsterSchema, db: Session = Depends(get_db)):
    """
    Update an existing monster based on the provided monster details.

    Args:
        monster_id (int): The monster ID.
        monster (PlainMonsterSchema): The monster details.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the updated monster details.

    """
    try:
        monster_to_update = db.query(Monster).filter(
            Monster.id == monster_id).first()

        if not monster_to_update:
            raise HTTPException(status_code=404, detail="Monster not found")

        for key, value in monster.model_dump(exclude_unset=True).items():
            setattr(monster_to_update, key, value)

        db.commit()

        return MonsterSchema.model_validate(monster_to_update)

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")


@router.delete('/{monster_id}')
def delete_monster(monster_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing monster based on the monster ID.

    Args:
        monster_id (int): The monster ID.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the success message.
    """
    try:
        monster = db.query(Monster).filter(Monster.id == monster_id).first()

        if not monster:
            raise HTTPException(status_code=404, detail="Monster not found")

        db.delete(monster)
        db.commit()

        return {"message": "Monster deleted successfully"}

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail="Oops! Something went wrong")
