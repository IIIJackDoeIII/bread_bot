# bread_bot
English Version
Keep Bot Always Active Using Replit and UptimeRobot

This project uses Replit to host the bot and UptimeRobot to keep the bot alive. Here's how it works:

Replit Hosting:

The bot runs on Replit, which provides a temporary URL (e.g., https://your-repl-url.replit.dev).
Replit automatically "sleeps" if it doesn't receive any activity for a while.
UptimeRobot Integration:

UptimeRobot is a free service that sends periodic requests (every 5 minutes) to your Replit URL.
These requests wake up Replit if it's sleeping, ensuring the bot remains active.
Setting Up:

Add a Flask (or similar) endpoint in your Replit project to respond to UptimeRobot's requests (e.g., I’m alive!).
Register the Replit URL in UptimeRobot for monitoring.
Dependencies:

Make sure you install all necessary dependencies using pip install -r requirements.txt.
Русская версия
Как заставить бота работать постоянно с помощью Replit и UptimeRobot

Этот проект использует Replit для размещения бота и UptimeRobot для того, чтобы бот оставался активным. Вот как это работает:

Размещение на Replit:

Бот работает на платформе Replit, которая предоставляет временный URL (например, https://your-repl-url.replit.dev).
Replit автоматически "засыпает", если долгое время не получает активности.
Интеграция с UptimeRobot:

UptimeRobot — это бесплатный сервис, который отправляет регулярные запросы (каждые 5 минут) на ваш URL.
Эти запросы "будят" Replit, если он уснул, что гарантирует, что бот остаётся доступным.
Настройка:

Добавьте Flask (или аналогичный) endpoint в ваш проект на Replit, чтобы отвечать на запросы UptimeRobot (например, I’m alive!).
Зарегистрируйте URL вашего Replit в UptimeRobot для мониторинга.
Зависимости:

Убедитесь, что все зависимости установлены с помощью pip install -r requirements.txt.