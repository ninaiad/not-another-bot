import asyncio
import wikipedia

from random import randint
from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = ""
storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

wikipedia.set_lang("en")

BOTS_NUM = 10

class TimerObj(StatesGroup):
    time = State()

class RequestObj(StatesGroup):
    wiki_request = State()

class GuessObj(StatesGroup):
    guess = State()

# HELP

@dp.message_handler(commands=['start', 'help'])
async def help(msg: types.Message):
    with open("utils/help.txt") as help_text:
        await msg.reply(help_text.read())

# CANCEL

@dp.message_handler(state="*", commands=['cancel'])
async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await msg.reply("No process to cancel.")

    await state.finish()
    return await msg.reply("Cancelled!")

# PLAY WITH ME

@dp.message_handler(commands=['play'])
async def play_with_me(msg: types.Message):
    await msg.reply("We're playing a guessing game! "
                    "I've picked a natural number from 0 to 10. Guess it.\n"
                    "Your guess should be a number, presented as a numeral, like so: 3")
    await GuessObj.guess.set()
    BOTS_NUM = randint(0, 10)

@dp.message_handler(lambda msg: not msg.text.isdigit(), state=GuessObj.guess)
async def check_a_guess_invalid(msg: types.Message, state: FSMContext):
    if (msg.text == "cancel" or msg.text == "/cancel"):
        await state.finish()
        return await msg.reply("Cancelled!")

    return await msg.reply("Your guess should be a number, presented as a numeral, like so: 3")

@dp.message_handler(lambda msg: msg.text.isdigit(), state=GuessObj.guess)
async def check_a_guess(msg: types.Message, state: FSMContext):
    if (int(msg.text) == BOTS_NUM):
        await state.finish()
        return await msg.reply("yep 🎉🎉🎉🎉")
    
    await msg.reply("nope.\ntry again! (if you don't want to play anymore, send 'cancel')")
    
# TIMER

@dp.message_handler(commands=['timer'])
async def set_timer(msg: types.Message):
    await TimerObj.time.set()
    return await msg.reply("How long would you like to set the timer for in minutes?")

@dp.message_handler(lambda msg: msg.text.isdigit(), state=TimerObj.time)
async def get_timer_input(msg: types.Message, state: FSMContext):
    await state.finish()

    await asyncio.sleep(60 * int(msg.text)) # is dying if data's wrong
    return await msg.reply("Time's up!")

@dp.message_handler(lambda msg: not msg.text.isdigit(), state=TimerObj.time)
async def get_timer_input_invalid(msg: types.Message, state: FSMContext):
    if (msg.text == "cancel" | msg.text == "/cancel"):
        await state.finish()
        return await msg.reply("Cancelled!")

    return await msg.reply("Time has to be a number.\nHow long would you like to set the timer for in minutes?")

# DEFINE

@dp.message_handler(commands=['define'])
async def find_definition(msg: types.Message):
    await RequestObj.wiki_request.set()
    await msg.reply("What would you like to find?")

@dp.message_handler(state=RequestObj.wiki_request)
async def find_definition(msg: types.Message, state: FSMContext):
    await state.finish()
    try:
        return await msg.reply(wikipedia.summary((msg.text).capitalize(), sentences=3))
    except:
        return await msg.reply("Definition not found!")

# OTHER

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.text.lower() == 'привет':
        await msg.reply("привет и тебе:)")
    elif msg.text.lower() == 'hi':
        await msg.reply("hi")
    elif msg.text.lower() == 'help':
        await help(msg)
    elif msg.text.lower() == 'play':
        await play_with_me(msg)
    elif msg.text.lower() == 'timer':
        await set_timer(msg)
    else:
       await msg.answer("This program doesn't exist. Use '/help' to view available programs.")

if __name__ == "__main__":
    executor.start_polling(dp)
