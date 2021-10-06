import asyncio
import sqlite3
from .admin_hub import admin_menu
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from buttons import faq_edit_markup, confirm_mailing_markup, admin_hub_markup
from loader import dp, bot, ADMINS

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@dp.callback_query_handler(text="mailing")
async def write_msg_mailing(call: CallbackQuery, state: FSMContext):
    text = "Отправьте сообщение для рассылки:"
    await state.set_state("write_msg_mailing")
    msg = await call.message.edit_text(text, reply_markup=faq_edit_markup)
    await state.update_data(mailing_msg=msg)
    await call.answer()


@dp.message_handler(state="write_msg_mailing", content_types=CONTENT_TYPES)
async def confirm_mailing(message: Message, state: FSMContext):
    data = await state.get_data()
    mailing_msg = data["mailing_msg"]
    await mailing_msg.delete()
    text = "Вы точно хотите разослать данное сообщение?"
    await state.set_state("confirm_mailing")
    await state.update_data(mailing_msg=message)
    msg = await message.answer(text, reply_markup=confirm_mailing_markup)
    await state.update_data(confirm_mailing_msg=msg)


@dp.callback_query_handler(text="yes_mailing", state="confirm_mailing")
async def mailing_msg_confirmed(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    confirm_mailing_msg = data["confirm_mailing_msg"]
    await confirm_mailing_msg.delete()
    mailing_msg = data["mailing_msg"]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    users_id = cs.execute("SELECT id FROM users")
    users_id = users_id.fetchall()
    for user in users_id:
        if user[0] == int(call.from_user.id):
            pass
        else:
            await bot.forward_message(from_chat_id=call.message.chat.id, message_id=mailing_msg.message_id,
                                      chat_id=user[0], disable_notification=False)

    msg = await call.message.answer("Готово!")
    await state.reset_state(with_data=True)
    await asyncio.sleep(0.7)
    await msg.delete()
    await admin_menu(call.message)
    await call.answer()


@dp.callback_query_handler(text="no_mailing", state="confirm_mailing")
async def mailing_msg_no_confirmed(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await call.message.edit_text("АДМИН-ПАНЕЛЬ", reply_markup=admin_hub_markup)
    await call.answer()
