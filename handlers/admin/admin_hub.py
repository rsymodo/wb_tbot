from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from buttons import admin_hub_markup
from loader import dp, ADMINS


@dp.message_handler(lambda x: x.from_user.id in ADMINS, commands=["admin"])
async def admin_menu(message: Message):
    text = "АДМИН-ПАНЕЛЬ"
    await message.answer(text, reply_markup=admin_hub_markup)


@dp.callback_query_handler(state="write_id_payment", text="back_to_admin_menu")
@dp.callback_query_handler(state="write_msg_mailing", text="back_to_admin_menu")
@dp.callback_query_handler(state="search_profile_with_number", text="back_to_admin_menu")
@dp.callback_query_handler(state="search_profile_with_id", text="back_to_admin_menu")
@dp.callback_query_handler(state="search_profile_with_email", text="back_to_admin_menu")
@dp.callback_query_handler(state="choose_type_search_profile", text="back_to_admin_menu")
@dp.callback_query_handler(text="no_DS", state="disable_system")
@dp.callback_query_handler(text="back_to_admin_menu", state="edit_contacts")
@dp.callback_query_handler(text="back_to_admin_menu", state="edit_faq")
@dp.callback_query_handler(text="back_to_admin_menu")
async def back_to_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await call.message.delete()
    await admin_menu(call.message)
    await call.answer()


@dp.callback_query_handler(text="close_admin_panel")
async def close_admin_panel(call: CallbackQuery):
    await call.message.delete()
    await call.answer()