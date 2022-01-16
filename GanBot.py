from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import *
from CycleGan.cycle.test_image import start_gan
import uuid

config = load_config("bot.ini")
bot = Bot(token=config.tg_bot.token)


class Gan(StatesGroup):
    waiting_for_model_name_P1 = State()
    waiting_for_model_name_P2 = State()
    waiting_for_photo = State()
    waiting_for_size_of_output_image = State()


async def gan_first(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*styles)
    await message.answer("Выберите стиль с клавиатуры снизу...", reply_markup=keyboard)
    await Gan.waiting_for_model_name_P1.set()


async def first_keyboard(message: types.Message, state: FSMContext):
    if message.text not in styles:
        await message.answer("Пожалуйста, выберите стиль изображения с клавиатуры снизу...")
        return
    if message.text in to_second_keyboard:
        if message.text == 'Апельсины 🔄 Яблоки':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*Apples2oranges)
            await message.answer("Выберите стиль с клавиатуры снизу...", reply_markup=keyboard)
            await Gan.next()
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*horses2zebras)
            await message.answer("Выберите стиль с клавиатуры снизу...", reply_markup=keyboard)
            await Gan.next()
    else:
        model = style2model[message.text]
        await state.update_data(model=model)
        await message.answer("Выберите фото, которое будет редактироваться...",
                             reply_markup=types.ReplyKeyboardRemove())
        await Gan.waiting_for_photo.set()


async def second_keyboard(message: types.Message, state: FSMContext):
    if message.text not in Apples2oranges and message.text not in horses2zebras:
        await message.answer("Пожалуйста, выберите стиль изображения с клавиатуры снизу...")
        return
    model = style2model[message.text]
    await state.update_data(model=model)
    await message.answer("Выберите фото, которое будет редактироваться...", reply_markup=types.ReplyKeyboardRemove())
    await Gan.next()


async def photo_chosen(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию.")
        return
    id = message.from_user.id
    unique_id = message.photo[-1].file_unique_id
    dir = direction_of_the_files + '/' + str(id) + '/' + str(unique_id) + '.jpg'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*quality)
    await message.photo[-1].download(destination_file=dir)
    await state.update_data(id_of_user=id, id_of_the_photo=unique_id)
    await message.answer("Теперь выберите размер качество изображения на клавиатуре снизу.", reply_markup=keyboard)
    await Gan.next()


async def size_of_the_image_chosen(message: types.Message, state: FSMContext):
    if not message.text and message.text.lower() not in quality:
        await message.answer("Пожалуйста, выберите качество изображение с клавиатуры")
        return
    size = quality_to_sizes[message.text.lower()]
    user_data = await state.get_data()
    direct_of_the_photos = direction_of_the_files + '/' + str(user_data['id_of_user'])
    await message.answer(f'Всё готово!\n'
                         f'Теперь осталось только подождать, когда изображение сгенерируется.\n',
                         reply_markup=types.ReplyKeyboardRemove())

    name_of_the_output = str(uuid.uuid4())
    direct_of_the_input = direct_of_the_photos + '/' + user_data['id_of_the_photo'] + '.jpg'
    direct_of_the_output = direct_of_the_photos + '/' + name_of_the_output + '.jpg'
    await start_gan(direct_of_the_input, user_data['model'], size, direct_of_the_output)

    await bot.send_photo(message.chat.id, types.InputFile(direct_of_the_output))
    await state.finish()


def register_handlers_gan(dp: Dispatcher):
    dp.register_message_handler(gan_first, commands="gan", state="*")
    dp.register_message_handler(first_keyboard, state=Gan.waiting_for_model_name_P1, content_types=content_types)
    dp.register_message_handler(second_keyboard, state=Gan.waiting_for_model_name_P2, content_types=content_types)
    dp.register_message_handler(photo_chosen, state=Gan.waiting_for_photo, content_types=content_types)
    dp.register_message_handler(size_of_the_image_chosen, state=Gan.waiting_for_size_of_output_image,
                                content_types=content_types)