from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from typing import Final

TOKEN: Final = "8062849575:AAGFAksPKDe3r-sW3tdZfY8di7hsDrq35fg"
BOT_USERNAME: Final = "@QuestionPoll2_bot"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("The bot is up and running.")

async def explanation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me a question followed by the answers. Format:\n"
        "Question\nAnswer 1\nAnswer 2\nAnswer 3\n...\nCorrect Answer (e.g., 'Answer 1')\nExplanation"
        "\n\nExample:\nWhat is the best programming language?\nPython\nJavaScript\nC++\nJava\nPython\nIt is the most used programming language in the world"
    )
async def no_explanation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me a question followed by the answers. Format:\n"
        "Question\nAnswer 1\nAnswer 2\nAnswer 3\n...\nCorrect Answer (e.g., 'Answer 1')\nno explanation"
        "\n\nExample:\nWhat is the best programming language?\nPython\nJavaScript\nC++\nJava\nPython\nno explanation"
    )


# async def example_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "What is the best programming language?\nPython\nJavaScript\nC++\nJava\nPython\nIt is the most used programming language in the world"
#     )

# Function to create a poll (quiz type)
async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    # Split the message by new lines
    question_and_answers = text.split("\n")

    # Ensure there are at least two lines (question and at least two answers)
    if len(question_and_answers) < 3:
        await update.message.reply_text("Please send a question followed by at least two answers.")
        return

    # # Ensure there are a maximum of 6 answers
    # if len(question_and_answers) > 7:
    #     await update.message.reply_text("You can only provide up to 6 answers. Please limit your answers.")
    #     return

    # The question is the first line
    question = question_and_answers[0]

    # The answers are all lines except the last one (which is the correct answer)
    # answers = question_and_answers[1:-2]
    answers = [answer.strip() for answer in question_and_answers[1: -2]]

    # The correct answer is the last line
    correct_answer = question_and_answers[-2].strip()

    #The explanation
    explanation = question_and_answers[-1]

    # Check if the correct answer is in the provided answers
    if correct_answer not in answers:
        await update.message.reply_text("The correct answer must be one of the provided answers.")
        return

    # Get the index of the correct answer
    correct_answer_index = answers.index(correct_answer)

    if 'no explanation' in explanation.lower():
        await update.message.reply_poll(
            question=question,
            options=answers,
            type=Poll.QUIZ,
            correct_option_id=correct_answer_index,
        )
    else:
        await update.message.reply_poll(
            question=question,
            options=answers,
            type=Poll.QUIZ,
            correct_option_id=correct_answer_index,
            explanation=explanation
        )


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # if message_type == 'group':
    #     if BOT_USERNAME in text:
    #         new_text: str = text.replace(BOT_USERNAME, '').strip()
    #         await create_poll(update, context, new_text)
    # else:
    #     await create_poll(update, context, text)

    if BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        await create_poll(update, context, new_text)
    else:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        await create_poll(update, context, new_text)


# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('no_explanation', no_explanation_command))
    app.add_handler(CommandHandler('explanation', explanation_command))
    # app.add_handler(CommandHandler('example', example_command))

    # Text Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
