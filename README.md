# Бот для хранения и поиска мемов

Данный бот позволяет пользователю сохранять изображения в базе, добавляя теги, а затем по этим тегам находить данное изображение.
Также реализована функция "Случайный мем", по которой бот скидывает рандомную картинку.

Пользователи из списка USERS могут использовать все функции, кроме добавления изображений - это доступно только пользователям из списка ADMINS.

## Технологии
1. Aiogram v3
2. Redis
3. PostgreSQL (асинхронное взаимодействие с БД)
4. SQLAlchemy
