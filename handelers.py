from config import dp
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
import text
import Game
import random

@dp.message_handler(commands=["start"])
async def on_start(message: Message):
    await message.answer(text=f"{message.from_user.first_name}"
                              f"{text.greeting}") 

@dp.message_handler(commands=["new_game"])
async def start_new_game(messege: Message):
    Game.new_game()
    if Game.check_game():
        toss = random.randint(0,1)
        if toss:
            await player_turn(messege)
        else:
            await bot_turn(messege)
        
async def player_turn(message: Message):
    await message.answer(f"{message.from_user.first_name},"
                        f"  твой ход! Сколько возимешь конфет ?")

@dp.message_handler()
async def take(message: Message):
    name = message.from_user.first_name
    if Game.check_game():
        if message.text.isdigit():
            take = int(message.text)
            if (0 < take < 29) and take <= Game.get_total():
                Game.take_candies(take)
                if await check_win(message, take, "player"):
                    return
                await message.answer(f"{name} взял {take} конфет, и на столье осталось " 
                                     f"{Game.get_total()}. Ход бота...")
                await bot_turn(message)

            else:
                await message.answer("Много взял! Можно не больше 28 за раз.")
        else:
            pass    

async def bot_turn(message):
    total = Game.get_total()
    if total <= 28:
        take = total
    else:
        take = random.randint(1,28)
    Game.take_candies(take)
    await message.answer(f"Бот взял {take} конфет и их осталось {Game.get_total()}")
    if await check_win(message,take,"Бот"):
        return
    await player_turn(message)


async def check_win(message, take: int, player: str):
    if Game.get_total()<=0:
        if player == "player":
            await message.answer(f"{message.from_user.first_name} взял {take} конфет и ПОБЕДИЛ!!!")
        else:
            await message.answer(f"Бот взял {take} конфет и ПОБЕДИЛ!!!")
        Game.new_game()
        return True
    else: return False