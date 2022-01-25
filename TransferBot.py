from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import load_config, content_types, direction_of_the_files, quality_to_sizes, quality
from TransferStyles import run_style_transfer_from_bot
import uuid

config = load_config("bot.ini")
bot = Bot(token=config.tg_bot.token)


class Trans(StatesGroup):
    waiting_for_first_photo = State()
    waiting_for_second_photo = State()
    waiting_for_size_of_output_image = State()


async def trans_first(message: types.Message):
    await message.answer("Пришлите фотографию, которую будут изменять...")
    await Trans.waiting_for_first_photo.set()


async def first_photo_chosen(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте первую фотографию.")
        print(message)
        return
    id = message.from_user.id
    unique_id = message.photo[-1].file_unique_id
    dir = direction_of_the_files + '/' + str(id) + '/' + str(unique_id) + '.jpg'
    await message.photo[-1].download(destination_file=dir)
    await state.update_data(id_of_user=id, id_of_the_first_photo=unique_id)
    await message.answer("Теперь отправьте фото, с которого будет браться стиль...")
    await Trans.next()


async def second_photo_chosen(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте вторую фотографию.")
        return
    id = message.from_user.id
    unique_id = message.photo[-1].file_unique_id
    dir = direction_of_the_files + '/' + str(id) + '/' + str(unique_id) + '.jpg'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*quality)
    await message.photo[-1].download(destination_file=dir)
    await state.update_data(id_of_the_second_photo=unique_id)
    await message.answer("Теперь выберите размер качество изображения на клавиатуре снизу.\n"
                         "Учтите, что это напрямую влияет на скорость получения результата....", reply_markup=keyboard)
    await Trans.next()


async def size_of_the_image_chosen(message: types.Message, state: FSMContext):
    if not message.text and message.text.lower() not in quality:
        await message.answer("Пожалуйста, выберите качество изображение с клавиатуры")
        return
    size = quality_to_sizes[message.text.lower()]
    user_data = await state.get_data()
    direct_of_the_photos = direction_of_the_files + '/' + str(user_data['id_of_user'])
    await message.answer(f'Всё готово!\n'
                         f'Теперь осталось только подождать, когда изображение сгенерируется.',
                         reply_markup=types.ReplyKeyboardRemove())

    msg = await message.answer(f'Здесь для удобства будет показываться прогресс генерации фотографии.\n'
                               f'Времени прошло с начала: 00:00...\n'
                               f'Примерное время ожидания: 00:00...\n'
                               f'Прогресс: 0%.....')

    name_of_the_output = str(uuid.uuid4())
    await run_style_transfer_from_bot(size, direct_of_the_photos,
                                      user_data['id_of_the_first_photo'],
                                      user_data['id_of_the_second_photo'], name_of_the_output, msg)

    direct_of_the_output = direct_of_the_photos + '/' + name_of_the_output + '.jpg'
    await bot.send_photo(message.chat.id, types.InputFile(direct_of_the_output))
    await state.finish()


def register_handlers_transfers(dp: Dispatcher):
    dp.register_message_handler(trans_first, commands="trans", state="*")
    dp.register_message_handler(first_photo_chosen, state=Trans.waiting_for_first_photo, content_types=content_types)
    dp.register_message_handler(second_photo_chosen, state=Trans.waiting_for_second_photo, content_types=content_types)
    dp.register_message_handler(size_of_the_image_chosen, state=Trans.waiting_for_size_of_output_image,
                                content_types=content_types)
