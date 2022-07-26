from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import UUID4
from .. import oauth2

from app import utils

from .. import conn, cr, models

router = APIRouter(tags=["/users"], prefix="/users")


@router.get("/", response_model=models.UserReturn | models.UserOut)
def get_users(id: UUID4 = Query(default=None), limit: int = Query(default=None)):
    if id == None:
        cr.execute(
            """ SELECT * FROM users Limit %s """,
            (None if limit is None else str(limit),),
        )
        users = cr.fetchall()
        return {"users": users}
    else:
        cr.execute("""SELECT * FROM users WHERE id = %s""", (str(id),))
        user = cr.fetchone()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} was not found",
            )
        return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.UserReturn)
def create_user(user_data: models.UserCreate):
    cr.execute(
        """ INSERT INTO users(id,username,password,created_at,total_transactions) VALUES (uuid_generate_v4(),%s,%s,%s,%s) RETURNING *""",
        (
            user_data.username,
            utils.hash(user_data.password),
            user_data.created_at,
            user_data.total_transactions,
        ),
    )
    user_created = cr.fetchone()
    conn.commit()
    return user_created


@router.delete("/")
def delete_user(current_user=Depends(oauth2.get_current_user)):
    cr.execute("""DELETE FROM users WHERE id=%s RETURNING *""", (str(current_user.id),))
    user_deleted = cr.fetchone()
    if not user_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id=} not found"
        )
    conn.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.put("/{id}")
def update_user(
    update_data: models.UserUpdate, current_user=Depends(oauth2.get_current_user)
):
    update_data = update_data.dict(exclude_unset=True)
    # todo find out how to loop and enter values in query automaticaly
    cr.execute(
        """UPDATE users SET {} WHERE id = %s RETURNING *""".format(
            ",".join([f"{key} = {value}" for key, value in update_data.items()])
        ),
        (current_user.id,),
    )
    user_updated = cr.fetchone()
    if not user_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id=} not found"
        )
    conn.commit()
    return user_updated
