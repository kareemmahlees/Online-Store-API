from turtle import update
from uuid import uuid4
from fastapi import APIRouter, Body, Query, HTTPException, Response, status
from pydantic import UUID4
from .. import conn, cr, models

router = APIRouter(tags=["product"], prefix="/products")


@router.get("/", response_model=models.ProductOut | models.Product)
def get_poroducts(id: UUID4 = Query(default=None), limit: int = Query(default=None)):
    if id == None:
        cr.execute(
            """ SELECT * FROM product Limit %s """,
            (None if limit is None else str(limit),),
        )
        products = cr.fetchall()
        return {"products": products}
    else:
        cr.execute("""SELECT * FROM product WHERE id = %s""", (str(id),))
        product = cr.fetchone()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} was not found",
            )
        return product


@router.post("/", response_model=models.Product, status_code=status.HTTP_201_CREATED)
def create_product(product_data: models.ProductIn):
    cr.execute(
        """INSERT INTO product(id,product_name,category,price,inventory,after_discount) VALUES (uuid_generate_v4(),%s,%s,%s,%s,%s) RETURNING *""",
        (
            product_data.product_name,
            product_data.category,
            product_data.price,
            product_data.inventory,
            product_data.after_discount,
        ),
    )
    product_created = cr.fetchone()
    return product_created


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: str):
    cr.execute(""" DELETE FROM product WHERE id = %s RETURNING *""", (id,))
    product_deleted = cr.fetchone()
    if not product_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=models.Product)
def update_product(id: str, product: models.ProductIn):
    update_data = product.dict(exclude_unset=True)
    # todo still in progress
    # cr.execute(
    #     """UPDATE product SET VALUES (%s) WHERE id=%s RETURNING *""",
    #     (
    # ",".join([key for key in update_data.keys()]),
    # ",".join([key for key in update_data.values()]),
    #         **update_data
    #         id,
    #     ),
    # )
    # product_updated = cr.fetchone()
    # if not product_updated:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Product with {id=} not found",
    #     )
    # return product_updated
