from aiogram import Bot, Dispatcher, executor, types
import asyncio, os

from keyboard import *
from db import *


async def checked_place_game(inline_id, place):
	room = get_game_room(inline_id=inline_id)[0]
	# room_place = json.loads(room[1])

	# print(place)
	if (place[0] == "⭕️" and place[4] == "⭕️" and place[8] == "⭕️") or (place[6] == "⭕️" and place[4] == "⭕️" and place[2] == "⭕️") or (place[0] == "⭕️" and place[1] == "⭕️" and place[2] == "⭕️") or (place[3] == "⭕️" and place[4] == "⭕️" and place[5] == "⭕️") or (place[6] == "⭕️" and place[7] == "⭕️" and place[8] == "⭕️") or (place[0] == "⭕️" and place[3] == "⭕️" and place[6] == "⭕️") or (place[1] == "⭕️" and place[4] == "⭕️" and place[7] == "⭕️") or (place[2] == "⭕️" and place[5] == "⭕️" and place[8] == "⭕️"):
		update_game_room(inline_id=inline_id, index="going", value="end")
		return await bot.edit_message_text(inline_message_id=inline_id, text=f"Выиграл <a href='tg://user?id={room[2]}'>⭕️</a>", parse_mode="HTML", reply_markup=update_inline_markup(inline_id, place))
		print("⭕️ win!")
	elif (place[0] == "❎" and place[4] == "❎" and place[8] == "❎") or (place[6] == "❎" and place[4] == "❎" and place[2] == "❎") or (place[0] == "❎" and place[1] == "❎" and place[2] == "❎") or (place[3] == "❎" and place[4] == "❎" and place[5] == "❎") or (place[6] == "❎" and place[7] == "❎" and place[8] == "❎") or (place[0] == "❎" and place[3] == "❎" and place[6] == "❎") or (place[1] == "❎" and place[4] == "❎" and place[7] == "❎") or (place[2] == "❎" and place[5] == "❎" and place[8] == "❎"):
		update_game_room(inline_id=inline_id, index="going", value="end")
		return await bot.edit_message_text(inline_message_id=inline_id, text=f"Выиграл <a href='tg://user?id={room[0]}'>❎</a>", parse_mode="HTML", reply_markup=update_inline_markup(inline_id, place))
		print("❎ win!!!")
	if "🔥" not in place:
		update_game_room(inline_id=inline_id, index="going", value="end")
		return await bot.edit_message_text(inline_message_id=inline_id, text=f"Ничья!", reply_markup=update_inline_markup(inline_id, place))
		print("Усё")	 

	await bot.edit_message_text(inline_message_id=inline_id, text="Крестики нолики", reply_markup=update_inline_markup(inline_id, place))

async def callback_handler_ticTacToe(call: types.CallbackQuery):
	if "plane_" in call.data:
		room = get_game_room(inline_id=call.inline_message_id)[0]
		room_place = json.loads(room[1])
		# room_place[int(call.data.split("plane_")[1])] = "❎"

		if room[4] == "end":
			await call.answer(text="Игра завершина", show_alert=True)
			try: return await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Игра завершина", reply_markup=update_inline_markup(call.inline_message_id, room_place))
			except Exception as e: print(e)

		if room[2] is None and call["from"].id == room[0]:
			print("hey")
			return await call.answer(text="Уступайте сопернику шаг, не нужно быть жадиной", show_alert=True)
			# await bot.answer_callback_query(callback_query_id=call.id, text="Уступайте сопернику шаг, не нужно быть жадиной", show_alert=1)  
		elif room[2] is None and call["from"].id != room[0]:
			update_game_room(inline_id=call.inline_message_id, index="player_2", value=call["from"].id)
			await bot.answer_callback_query(callback_query_id=call.id, text="Вы начали игру! Вы играете за ⭕️")
			room_place[int(call.data.split("plane_")[1])] = "⭕️"
			update_game_room(inline_id=call.inline_message_id, index="going", value=room[0])

		if room[4] is not None and room[4] != call["from"].id:
			return await bot.answer_callback_query(callback_query_id=call.id, text="Сейчас ходит соперник, йоу")
		
		if room[4] == call["from"].id and call["from"].id == room[0]:
			update_game_room(inline_id=call.inline_message_id, index="going", value=room[2])
			room_place[int(call.data.split("plane_")[1])] = "❎"
		else: 
			update_game_room(inline_id=call.inline_message_id, index="going", value=room[0])
			room_place[int(call.data.split("plane_")[1])] = "⭕️"

		await checked_place_game(call.inline_message_id, room_place)

	if call.data == "restart_zero_game":
		room = get_game_room(inline_id=call.inline_message_id)[0]
		update_game_room(inline_id=call.inline_message_id, index="going", value=room[2])
		update_game_room(inline_id=call.inline_message_id, index="place", value=json.dumps(["🔥" for _ in range(9)]))
		return await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Крестики нолики\nПервый ходит <a href='tg://user?id={room[2]}'>соперник</a>", parse_mode="HTML", reply_markup=start_markup())
	elif call.data == "delete_zero_game":
		room = get_game_room(inline_id=call.inline_message_id)[0]
		await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Круто поиграли ☺️")
		delete_game_room(inline_id=call.inline_message_id)
		return await call.answer(text="Игра была удалена из чата")

	await call.answer()


# if __name__ == '__main__':
# 	executor.start_polling(dp, skip_updates=True)