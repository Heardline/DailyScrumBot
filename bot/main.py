import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import config
from database import init_db, add_report, get_reports_for_sprint
from report import create_markdown_report

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для сбора отчетов по методологии Scrum. Отправь мне свой отчет, и я сохраню его.")

def handle_report(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data = {
        'first_name': update.message.from_user.first_name,
        'last_name': update.message.from_user.last_name
    }
    report_text = update.message.text
    submission_date = update.message.date

    # Здесь можно добавить логику для извлечения номера спринта из текста отчета или другим способом.
    sprint_number = 1

    # Сохранение отчета в базе данных
    add_report(user_id, sprint_number, report_text, submission_date)

    update.message.reply_text("Отчет успешно сохранен!")

def send_reports(update: Update, context: CallbackContext):
    # Извлечение данных об отчетах для определенного спринта из базы данных
    sprint_number = 1
    reports_data = get_reports_for_sprint(sprint_number)

    for report_data in reports_data:
        user_id, _, report_text, submission_date = report_data
        user_data = {'first_name': 'Имя', 'last_name': 'Фамилия'}  # Здесь можно добавить логику для получения имени и фамилии пользователя из базы данных

        # Формирование отчета в формате Markdown
        markdown_report = create_markdown_report(user_data, {'sprint_number': sprint_number, 'report_text': report_text})

        # Отправка отчета в формате Markdown
        update.message.reply_text(markdown_report, parse_mode='Markdown')

def main():
    init_db()

    updater = Updater(token=config.TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("send_reports", send_reports))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_report))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()