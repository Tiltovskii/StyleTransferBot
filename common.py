from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
import aiogram.utils.markdown as fmt


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer_sticker(sticker="CAACAgIAAxkBAAIE42HO3JzWgpKC2LFIGlXz0m3SDxbkAAL_AgACbbBCAwSgOas0AjY3IwQ")
    await message.answer(
        f"{fmt.hbold('Здравствуй')}, данный телеграмм бот может пренести"
        f" {fmt.hunderline('стиль')} одной фотографии на другую!\n"
        f"Чтобы воспользоваться самим ботом выберите, "
        f"какой моделью хотите воспользоваться: \n"
        f"1) Предобученной (/pretrained), но результат может вас не удовлетворить. \n"
        f'2) Обучить "с нуля" (/trans), но время работы может достигать 30 мин. при высоком разрешении.\n'
        f'3) Воспользоваться какими-то готовыми моделями (/gan), которые могут заменить, к примеру, апельсины на яблоки.\n',
        reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.HTML
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands=["start", "help"], state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
