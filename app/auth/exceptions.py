from fastapi import HTTPException, status


EXCEPTION_INCORRECT_USER_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

EXCEPTION_COULD_NOT_VALIDATE = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

EXCEPTION_INACTIVE_USER = HTTPException(status_code=400, detail="Inactive user")