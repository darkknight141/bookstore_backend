from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.carts.schemas import CartsSchema, CreateCart, UpdateCart, RetrieveCart, GetAddedBookFromCart
from api.carts.services import CartsService
from api.security import verify_token

oauth2_scheme = HTTPBearer()
carts_router = APIRouter(tags=['Carts'], dependencies=[Depends(oauth2_scheme)])


@carts_router.get('/carts/', response_model=RetrieveCart)
async def get_cart(
        user=Depends(verify_token),
        service: CreateCart = Depends(CartsService.from_request),
):
    return await service.get_cart(user)


@carts_router.post('/carts/', response_model=GetAddedBookFromCart)
async def add_book_to_cart(
        cart_data: CreateCart,
        user=Depends(verify_token),
        service: CartsService = Depends(CartsService.from_request)
):
    return await service.add_book_to_cart(cart_data, user)


@carts_router.patch('/carts/{book_id}')
async def update_book_from_cart(
        cart_data: UpdateCart,
        book_id: int,
        user=Depends(verify_token),
        service: CartsService = Depends(CartsService.from_request)
):
    return await service.update_book_from_cart(book_id, user, cart_data)


@carts_router.delete('/carts/{book_id}', status_code=204)
async def delete_book_from_cart(
        book_id: int,
        user=Depends(verify_token),
        service: CartsService = Depends(CartsService.from_request)
):
    return await service.delete_book_from_cart(book_id, user)
