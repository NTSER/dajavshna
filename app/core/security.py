from fastapi.security import OAuth2PasswordBearer

seller_oath2_scheme = OAuth2PasswordBearer("/seller/login")
consumer_oath2_scheme = OAuth2PasswordBearer("/consumer/login")
