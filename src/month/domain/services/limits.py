from src.sql_alchemy_repository  import IRepositoryBase
from src.user.data.repositories.user import UserRepository
from src.month.data.repositories import MonthRepository
from src.month.data.models import Month

import copy


class LimitsService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()

    async def set_day_limit(self, month: Month, day: int, limit: float) -> Month:
        if str(day) not in month.days_statistics:
            raise Exception(f"There is no day number {day} in the month")
        
        month.days_statistics = copy.deepcopy(month.days_statistics)

        month.days_statistics[str(day)]["limit"] = limit
        month.days_statistics[str(day)]["money_rest"] = limit - month.days_statistics[str(day)]["total_expenses"]
        
        month.savings += month.days_statistics[str(day)]["savings_taken"]
        month.days_statistics[str(day)]["savings_taken"] = 0

        return await self.month_repo.update(month)
    
    async def set_limits_after_day(self, month: Month, begin_day: int, limit: float) -> Month:
        if str(begin_day) not in month.days_statistics:
            raise Exception(f"There is no day number {begin_day} in the month")

        month.days_statistics = copy.deepcopy(month.days_statistics)
        for day in month.days_statistics:
            if int(day) >= begin_day:
                month.days_statistics[str(day)]["limit"] = limit
                month.days_statistics[str(day)]["money_rest"] = limit - month.days_statistics[str(day)]["total_expenses"]

                month.savings += month.days_statistics[str(day)]["savings_taken"]
                month.days_statistics[str(day)]["savings_taken"] = 0

        return await self.month_repo.update(month)

    async def transfer_limits(self, month: Month, limits: dict[str, float]) -> None:
        month.days_statistics = copy.deepcopy(month.days_statistics)

        # check sums
        old_sum_limit = sum([props["limit"] for day, props in month.days_statistics.items()])
        new_sum_limit = sum(limits.values())
        if old_sum_limit != new_sum_limit or len(month.days_statistics) != len(limits):
            raise Exception("Limits is incorrect")
        
        # check days
        for day in month.days_statistics:
            if str(day) not in limits:
                raise Exception(f"Day {str(day)} not specified")

        # recalculation of limits, money_rest
        for day in month.days_statistics:
            old_limit = month.days_statistics[str(day)]["limit"]
            month.days_statistics[str(day)]["money_rest"] += (limits[str(day)] - old_limit)
            month.days_statistics[str(day)]["limit"] = limits[str(day)]
        await self.month_repo.update(month)
