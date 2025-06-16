from .user import UserCreate, UserPublic, UserUpdate


class SellerPublic(UserPublic):
    pass


class SellerCreate(UserCreate):
    pass


class SellerUpdate(UserUpdate):
    pass
