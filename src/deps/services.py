from src.repository.user import UserRepository
from src.services.user import UserService

from src.repository.month import MonthRepository
from src.services.month import MonthService


def get_user_service():
    return UserService()

def get_month_service():
    return MonthService()