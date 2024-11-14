from random import randint
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from config import BOT_TOKEN, ATTEMPTS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}


@dp.message(CommandStart())
async def start_command(message: Message):
    if user['in_game']:
        await message.answer('Вы уже в игре')
    else:
        user['in_game'] = True
        user['secret_number'] = randint(1, 50)
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Отлично! Начинаем игру!\nЯ загадал число от 1 до 50, попробуй угадать\n'
            'У тебя есть 5 попыток'
        )


@dp.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer('Это простая игра, я загадываю число от 1 до 50, а ты угадываешь.\n'
                         'У тебя есть 5 попыток, если не получится то можно сыграть еще\n'
                         '\nДоступные команды:\n /start - начать игру\n /help - правила\n/cancel - выйти из игры\n'
                         '/stat - посмотреть статистику\n\nДавай сыграем?')


@dp.message(lambda x: x.text and x.text.isdigit() and user['in_game'])
async def numbers_command(message: Message):
    num = int(message.text)
    if  num < 1 or num > 50:
        await message.answer('Загадано число от 1 до 50')
    elif num == user['secret_number']:
        user['in_game'] = False
        user['total_games'] += 1
        user['wins'] += 1
        await message.answer(f'Ура Вы угадали!\nПоздравляю с победой!\nСыграем еще?')
    elif user['attempts'] == 1:
        user['attempts'] = None
        user['total_games'] += 1
        user['in_game'] = False
        await message.answer(
            f'В этот раз не получилось. Было загадано число {user['secret_number']}\nСыграем еще?')
    elif user['attempts'] > 1:
        user['attempts'] -= 1
        await message.answer(
            f'Загаднное число {['меньше', 'больше'][int(message.text) < user['secret_number']]} чем {message.text}')


@dp.message(Command(commands='stat'))
async def stat_command(message: Message):
    await message.answer(
        f'Всего игр: {user["total_games"]}\nПобед: {user["wins"]}'
        f'\nУдачных попыток: {user["total_games"]*100//user["wins"]}')


@dp.message()
async def other_command(message: Message):
    await message.answer('Используйте комманду /help, чтобы посмотреть что я умею')


if __name__ == '__main__':
    dp.run_polling(bot)
