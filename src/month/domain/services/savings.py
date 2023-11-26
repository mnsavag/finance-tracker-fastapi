from src.sql_alchemy_repository  import IRepositoryBase
from src.user.data.repositories.user import UserRepository
from src.month.data.repositories import MonthRepository
from src.month.data.models import Month

import copy


class SavingsService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()
    
    async def transfer_to_savings(self, month: Month, day: int, amount: float) -> Month:
        if str(day) not in self.days_statistics:
            raise Exception(f"There is no day number {day} in the month")

        month.days_statistics = copy.deepcopy(month.days_statistics)
        if month.days_statistics[str(day)]["money_rest"] >= amount:
            month.days_statistics[str(day)]["money_rest"] -= amount
            month.days_statistics[str(day)]["savings_taken"] -= amount
            month.savings += amount
        else:
            raise Exception("The balance is less than the entered amount")
        return await self.month_repo.update(month)
    
    async def transfer_from_savings(self, month: Month, day: int, amount: float) -> Month:
        if str(day) not in month.days_statistics:
            raise Exception(f"There is no day number {day} in the month")

        month.days_statistics = copy.deepcopy(month.days_statistics)

        if month.savings >= amount:
            month.savings -= amount
            month.days_statistics[str(day)]["savings_taken"] += amount
            month.days_statistics[str(day)]["money_rest"] += amount
        else:
            raise Exception("The savings is less than the entered amount")
        return await self.month_repo.update(month)

    async def rest_to_savings(self, month: Month, until_day: int) -> Month:
        if str(until_day) not in month.days_statistics:
            raise Exception(f"There is no day number {day} in the month")

        month.days_statistics = copy.deepcopy(month.days_statistics)
        for day in month.days_statistics:
            if int(day) == until_day:
                return
            month.days_statistics[str(day)]["profit"] += month.days_statistics[str(day)]["money_rest"]

            month.savings += month.days_statistics[str(day)]["money_rest"]
            month.days_statistics[str(day)]["money_rest"] = 0
        return await self.month_repo.update(month)
    
    async def rest_in_a_day(self, month: Month, until_day: int) -> Month:
        if str(until_day) not in month.days_statistics:
            raise Exception(f"There is no day number {day} in the month")
        
        month.days_statistics = copy.deepcopy(month.days_statistics)
        for day in month.days_statistics:
            if int(day) == until_day:
                return
            month.days_statistics[str(day)]["profit"] += month.days_statistics[str(day)]["money_rest"]

            month.days_statistics[str(until_day)]["money_rest"] += month.days_statistics[str(day)]["money_rest"] 
            month.days_statistics[str(until_day)]["limit"] += month.days_statistics[str(day)]["money_rest"]
            month.days_statistics[str(day)]["money_rest"] = 0
        return await self.month_repo.update(month)
