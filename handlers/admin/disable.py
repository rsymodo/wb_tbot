from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from buttons import confirm_disable_system_markup

from loader import dp


@dp.callback_query_handler(text="disable_bot")
async def disable_system_menu(call: CallbackQuery, state: FSMContext):
    text = "Вы точно хотите отключить бота?"
    await state.set_state("disable_system")
    await call.message.edit_text(text, reply_markup=confirm_disable_system_markup)
    await call.answer()


@dp.callback_query_handler(text="yes_DS", state="disable_system")
async def disable_system(call: CallbackQuery, state: FSMContext):
    await call.answer()
    dp.stop_polling()
