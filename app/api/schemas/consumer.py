from .user import UserCreate, UserPublic, UserUpdate


class ConsumerPublic(UserPublic):
    pass


class ConsumerCreate(UserCreate):
    pass


class ConsumerUpdate(UserUpdate):
    pass
