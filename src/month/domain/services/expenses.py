from src.sql_alchemy_repository  import IRepositoryBase
from src.user.data.repositories.user import UserRepository
from src.month.data.repositories import MonthRepository
from src.month.data.models import Month
from src.month.domain.schemas.month import DayExpenseCreate, DayExpenseDelete

import copy


class ExpensesService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()
    
    async def add_expense(self, month: Month, day: int, expense: DayExpenseCreate) -> Month:
        month.days_statistics = copy.deepcopy(month.days_statistics)

        month.days_statistics[str(day)]["total_expenses"] += expense.cost
        month.days_statistics[str(day)]["money_rest"] -= expense.cost

        if expense.name not in month.days_statistics[str(day)]["expenses"]:
            month.days_statistics[str(day)]["expenses"][expense.name] = 0

        month.days_statistics[str(day)]["expenses"][expense.name] += expense.cost
        month.total_expenses += expense.cost
       
        return await self.month_repo.update(month)
    
    async def delete_expense(self, month: Month, day: int, expense: DayExpenseDelete) -> Month:
        if expense.name not in month.days_statistics[str(day)]["expenses"]:
            raise Exception(f"{expense.name} not found")
        
        month.days_statistics = copy.deepcopy(month.days_statistics)
        cost = month.days_statistics[str(day)]["expenses"][expense.name]

        month.days_statistics[str(day)]["total_expenses"] -= cost
        month.days_statistics[str(day)]["money_rest"] += cost
        del month.days_statistics[str(day)]["expenses"][expense.name]
        month.total_expenses -= cost

        return await self.month_repo.update(month)
