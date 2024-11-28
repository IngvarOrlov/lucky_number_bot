from random import randint
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from config import BOT_TOKEN, ATTEMPTS
from model import Base, User


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
engine = create_engine('sqlite:///db.sqlite3', echo=True)
# user = {'in_game': False,
#         'secret_number': None,
#         'attempts': None,
#         'total_games': 0,
#         'wins': 0}

def get_user(message, session)->User:
    user = session.get(User, message.from_user.id)
    if not user:
        user = User(id=message.from_user.id, wins=0, total_games=0, in_game=False, attempts=0, secret_number=0)
        session.add(user)
        session.commit()
    return user


@dp.message(CommandStart())
async def start_command(message: Message):
    with Session(engine) as session:
        user = get_user(message, session)

        if user.in_game:
            await message.answer('Вы уже в игре')
        else:
            user.in_game = True
            user.secret_number = randint(1, 50)
            user.attempts = ATTEMPTS
        await message.answer(
            'Отлично! Начинаем игру!\nЯ загадал число от 1 до 50, попробуй угадать\n'
            'У тебя есть 5 попыток'
        )
        session.commit()

@dp.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer('Это простая игра, я загадываю число от 1 до 50, а ты угадываешь.\n'
                         'У тебя есть 5 попыток, если не получится то можно сыграть еще\n'
                         '\nДоступные команды:\n /start - начать игру\n /help - правила\n/cancel - выйти из игры\n'
                         '/stat - посмотреть статистику\n\nДавай сыграем?')


@dp.message(lambda x: x.text and x.text.isdigit())
async def numbers_command(message: Message):
    with Session(engine) as session:
        user = get_user(message, session)
        num = int(message.text)
        if not user.in_game:
            await message.answer("Для того чтобы начать игру, используй команду /start")
        elif num < 1 or num > 50:
            await message.answer('Загадано число от 1 до 50')
        elif num == user.secret_number:
            user.in_game = False
            user.total_games += 1
            user.wins += 1
            user.attempts == 0
            await message.answer(f'Ура Вы угадали!\nПоздравляю с победой!\nСыграем еще?')
            session.commit()
        elif user.attempts == 1:
            user.attempts = 0
            user.total_games += 1
            user.in_game = False
            await message.answer(
                f'В этот раз не получилось. Было загадано число {user.secret_number}\nСыграем еще?')
            session.commit()
        elif user.attempts > 1:
            user.attempts -= 1
            await message.answer(
                f'Загаднное число {['меньше', 'больше'][int(message.text) < user.secret_number]} чем {message.text}')
            session.commit()

@dp.message(Command(commands='stat'))
async def stat_command(message: Message):
    with Session(engine) as session:
        user = get_user(message, session)
        await message.answer(
            f'Всего игр: {user.total_games}\nПобед: {user.wins}'
            f'\nУдачных попыток: {round(100 // user.total_games  * user.wins)}%')


@dp.message()
async def other_command(message: Message):
    await message.answer('Используйте комманду /help, чтобы посмотреть что я умею')


if __name__ == '__main__':
    dp.run_polling(bot)
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
