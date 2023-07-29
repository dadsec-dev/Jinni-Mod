import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


# Load the environment variables from the .env file
load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = '@Ijaniki_Bot'

# Initialize the language model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo-16k",
    temperature=0.9
)

# Template for the bot's response
template = """
You are the community manager for an innovative cryptocurrency project called JinniAI, we are building a hyper-intelligent AI ecosystem which will be used in several domains, fashion, Ai assistant, whatsapp wallet etc, your name is Jinni. We have been Audited and have done our KYC with coinscope. Your aim is to thoughtfully address every user's {question}, make sure to keep reply clear and concise not lenghty. Users can only buy our token on Uniswap.
Contract Address or ca: 0x0fbf91A2282ADaaC4cCF0969b052b825FD3009C9
we are currently applying to Coingecko and awaiting their response. We have been listed on coinmarketcap, and people can track toke price here https://coinmarketcap.com/currencies/jinni-ai/
Website: https://www.0xjinni.ai/
Total supply: 10 billion. remember to keep things clear and concise, do not give info more than what was asked.
"""

# Create a prompt using the template
prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

# Create the language model chain
chain = LLMChain(llm=llm, prompt=prompt)


# Handle Responses
async def handle_response(text: str) -> str:
    # Pass the user's message through the language model chain
    response = chain.run({"question": text})

    # Return the response from the language model
    return response


# Telegram Bot Handlers

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey there!, I'm the community manager for the Jinni cryptocurrency project.")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What wallet do you wish to scan ?');

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can thoughtfully address any user's questions related to the Jinni project. Feel free to ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if the bot's username is mentioned in the message
    if BOT_USERNAME in text:
        # Remove the bot's username from the message text
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        response: str = await handle_response(new_text)

        print('Bot: ', response)
        await update.message.reply_text(response)
    else:
        # If the bot's username is not mentioned, do not respond
        print('Bot: No response - Bot not tagged')



# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type: str = update.message.chat.type
#     text: str = update.message.text
#
#     print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
#
    # Check if the bot's username is mentioned in the message
    # if BOT_USERNAME in text:
    #     # Remove the bot's username from the message text
    #     new_text: str = text.replace(BOT_USERNAME, '').strip()
    #     response: str = await handle_response(new_text)
    #
    #     print('Bot: ', response)
    #     await update.message.reply_text(response)
    # else:
    #     # If the bot's username is not mentioned, do not respond
    #     print('Bot: No response - Bot not tagged')

async def err(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused the following error {context.error}')


if __name__ == '__main__':
    print('Starting Bot ... ')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(err)

    print('Polling...')
    app.run_polling(poll_interval=3)
