from core import models, forms
from core.services.base import CRUDService


class UserService(CRUDService):
    pass


user_service: UserService = UserService(model=models.User, form=forms.RegistrationForm)
