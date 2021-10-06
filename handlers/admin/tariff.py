import asyncio
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from buttons import management_tariff_markup, back_to_management_tariff_markup, confirm_add_tariff_markup, \
    confirm_del_tariff_markup
from .admin_hub import admin_menu

from loader import dp


@dp.callback_query_handler(text="management_tariff")
async def management_tariff(call: CallbackQuery):
    text = "Управление тарифами"
    await call.message.edit_text(text, reply_markup=management_tariff_markup)
    await call.answer()


@dp.callback_query_handler(state="confirm_del_tariff", text="no_del_tariff")
@dp.callback_query_handler(state="confirm_new_tariff", text="no_add_tariff")
@dp.callback_query_handler(text="back_to_management_tariff", state="write_name_new_tariff")
@dp.callback_query_handler(text="back_to_management_tariff", state="write_description_new_tariff")
@dp.callback_query_handler(text="back_to_management_tariff", state="write_price_new_tariff")
@dp.callback_query_handler(text="back_to_management_tariff", state="write_count_new_tariff")
@dp.callback_query_handler(text="back_to_management_tariff", state="choose_tariff_for_delete")
async def cancel_add_new_tariff(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await call.message.delete()
    text = "Управление тарифами"
    await call.message.answer(text, reply_markup=management_tariff_markup)
    await call.answer()


# ---------------------------------------------------
# ---------------ЭТАПЫ ДОБАВЛЕНИЯ ТАРИФА-------------
@dp.callback_query_handler(text="add_tariff")
async def write_name_tariff(call: CallbackQuery, state: FSMContext):
    await state.set_state("write_name_new_tariff")
    text = "Введите название нового тарифа:"
    msg = await call.message.edit_text(text, reply_markup=back_to_management_tariff_markup)
    await state.update_data(WNNT_msg=msg)
    await call.answer()


@dp.message_handler(content_types=["text"], state="write_name_new_tariff")
async def write_description_tariff(message: Message, state: FSMContext):
    await state.set_state("write_description_new_tariff")
    await state.update_data(name_new_tariff=message.text)
    data = await state.get_data()
    WNNT_msg = data["WNNT_msg"]
    await WNNT_msg.delete()
    text = "Введите описание нового тарифа:"
    msg = await message.answer(text, reply_markup=back_to_management_tariff_markup)
    await state.update_data(WDNT_msg=msg)


@dp.message_handler(content_types=["text"], state="write_description_new_tariff")
async def write_price_tariff(message: Message, state: FSMContext):
    await state.set_state("write_price_new_tariff")
    await state.update_data(description_new_tariff=message.text)
    data = await state.get_data()
    WDNT_msg = data["WDNT_msg"]
    await WDNT_msg.delete()
    text = """Введите стоимость нового тарифа:
Примеры: 6 или 6.9(РУБ)
    """
    msg = await message.answer(text, reply_markup=back_to_management_tariff_markup)
    await state.update_data(WPNT_msg=msg)


@dp.message_handler(content_types=["text"], state="write_price_new_tariff")
async def write_count_tariff(message: Message, state: FSMContext):
    try:
        float(message.text)
    except Exception:
        msg = await message.answer("Неверный формат!Повторите попытку:")
        await asyncio.sleep(1)
        await msg.delete()
    else:
        await state.set_state("write_count_new_tariff")
        await state.update_data(price_new_tariff=message.text)
        data = await state.get_data()
        WPNT_msg = data["WPNT_msg"]
        await WPNT_msg.delete()
        text = "Введите количество выкупов нового тарифа:"
        msg = await message.answer(text, reply_markup=back_to_management_tariff_markup)
        await state.update_data(WCNT_msg=msg)


@dp.message_handler(content_types=["text"], state="write_count_new_tariff")
async def confirm_new_tarif(message: Message, state: FSMContext):
    try:
        float(message.text)
    except Exception:
        msg = await message.answer("Неверный формат!Повторите попытку:")
        await asyncio.sleep(1)
        await msg.delete()
    else:
        await state.set_state("confirm_new_tariff")
        await state.update_data(count_new_tariff=message.text)
        data = await state.get_data()
        WCNT_msg = data["WCNT_msg"]
        await WCNT_msg.delete()
        name = data["name_new_tariff"]
        description = data["description_new_tariff"]
        price = data["price_new_tariff"]
        text = """
Название: {name}
Описание: {description}
Цена: {price} ₽
Кол-во выкупов: {count} шт.

Вы уверены, что хотите добавить данный тариф?
""".format(count=message.text, price=price, description=description, name=name)
        msg = await message.answer(text, reply_markup=confirm_add_tariff_markup)
        await state.update_data(CNT_msg=msg)


@dp.callback_query_handler(state="confirm_new_tariff", text="yes_add_tariff")
async def confirmed_new_tariff(call: CallbackQuery, state: FSMContext):
    async def completing_add_tariff(call: CallbackQuery, state: FSMContext):
        CNT_msg = data["CNT_msg"]
        await CNT_msg.delete()
        await state.reset_state(with_data=True)
        msg = await call.message.answer("Готово!")
        await asyncio.sleep(0.5)
        await msg.delete()
        text = "Управление тарифами"
        await call.message.answer(text, reply_markup=management_tariff_markup)
        await call.answer()
        return

    data = await state.get_data()
    name = data["name_new_tariff"]
    description = data["description_new_tariff"]
    price = data["price_new_tariff"]
    count = data["count_new_tariff"]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    count_all_tariff = cs.execute(f"SELECT * FROM tariff")
    count_all_tariff = count_all_tariff.fetchall()
    if count_all_tariff == list():
        cs.execute(f"INSERT INTO tariff VALUES(1,'{name}','{description}','{price}',{count})")
        connect.commit()
        connect.close()
        await completing_add_tariff(call, state)
        return
    last_id = count_all_tariff[-1][0]
    cs.execute(
        f"INSERT INTO tariff(id,name,description,price,count) VALUES({last_id + 1},'{name}','{description}','{price}',{count})")
    connect.commit()
    connect.close()
    await completing_add_tariff(call, state)


# ---------------------------------------------------
# ---------------ЭТАПЫ УДАЛЕНИЯ ТАРИФА---------------

@dp.callback_query_handler(text="del_tariff")
async def show_tariff_for_delete(call: CallbackQuery, state: FSMContext):
    text = "Выберете тариф, который хотите удалить:"
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    all_tariff = cs.execute("SELECT * FROM tariff")
    all_tariff = all_tariff.fetchall()
    if all_tariff == list():
        msg = await call.message.answer("На данный момент тарифов нет!")
        await asyncio.sleep(0.7)
        await msg.delete()
        await call.answer()
        return
    all_tariff_markup = InlineKeyboardMarkup()
    for tariff in all_tariff:
        name = tariff[1]
        price = tariff[3]
        count = tariff[-1]
        all_tariff_markup.add(InlineKeyboardButton(text=f"{name} | {price + '₽'} | Кол-во выкупов: {count} шт.",
                                                   callback_data=f"tariff_{tariff[0]}"))
    all_tariff_markup.add(InlineKeyboardButton(text="Назад", callback_data="back_to_management_tariff"))
    await state.set_state("choose_tariff_for_delete")
    await call.message.edit_text(text, reply_markup=all_tariff_markup)
    await call.answer()


@dp.callback_query_handler(lambda x: "tariff_" in x.data, state="choose_tariff_for_delete")
async def confirm_del_tariff(call: CallbackQuery, state: FSMContext):
    tariff_id = call.data.split("_")[1]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    tariff_name = cs.execute(f"SELECT name FROM tariff WHERE id={tariff_id}")
    tariff_name = tariff_name.fetchone()[0]
    text = f"""
ID Тарифа: {tariff_id}
Название: {tariff_name}

Вы точно хотите удалить данный тариф?
    """
    await state.set_state("confirm_del_tariff")
    await state.update_data(tariff_id_for_del=tariff_id)
    await call.message.edit_text(text, reply_markup=confirm_del_tariff_markup)
    await call.answer()


@dp.callback_query_handler(text="yes_del_tariff", state="confirm_del_tariff")
async def confirmed_del_tariff(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tariff_id = data["tariff_id_for_del"]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    cs.execute(f"DELETE FROM tariff WHERE id={tariff_id}")
    connect.commit()
    connect.close()
    await state.reset_state(with_data=True)
    await call.message.delete()
    msg = await call.message.answer("Готово!")
    await asyncio.sleep(0.7)
    await msg.delete()
    text = "Управление тарифами"
    await call.message.answer(text, reply_markup=management_tariff_markup)
    await call.answer()
