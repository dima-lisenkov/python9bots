from aiogram import executor
from handelers import dp
async def on_startup(_):
    print("Бот запущен!")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_startup)