from aiogram.filters import BaseFilter
from aiogram.types import Message


class FilterNums(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, int]:
        lst = [i.replace('.','').replace(',', '').strip() for i in message.text.split()]
        filtered_nums = tuple(filter(lambda i: i.isdigit(), lst))
        if len(filtered_nums) == 1:
            return {'num': int(filtered_nums[0])}
        return False



