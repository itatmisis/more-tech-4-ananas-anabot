from aiogram import types
from aiogram.dispatcher.filters import Text
from anabot.keyboards.default import digest_menu, registration_menu
from anabot.loader import dp
from anabot.states.registration_states import RegistrationState
from anabot.loader import api
from anabot.utils.db_api.models import User


@dp.message_handler(Text(equals=["Регистрация"]), state=None)
async def start_registration(message: types.Message):
    await message.answer("Выберите свою роль:\n", reply_markup=registration_menu.role_selection_menu)
    await RegistrationState.role.set()


@dp.message_handler(Text(equals=["Бухгалтер", "Генеральный директор"]), state=RegistrationState.role)
async def source_selection(message: types.Message):
    user = User(message.from_user.id, 1 if message.text == "Бухгалтер" else 2)
    api.registration(user)
    answer = "Процесс регистрации окончен\nТеперь вы можете ознакомиться с самыми горячими новостями"
    await message.answer(answer, reply_markup=digest_menu.digest_menu)
    await RegistrationState.next()
