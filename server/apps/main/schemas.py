from djantic import ModelSchema

from apps.main.models import Ad, User


class AdSchema(ModelSchema):
    """Схема объявления для pydantic."""
    class Config:
        model = Ad
        include = ('id', 'title', 'seller', 'url')


class UserSchema(ModelSchema):
    """Схема пользователя для pydantic."""
    class Config:
        model = User
        include = ('id', 'email')
