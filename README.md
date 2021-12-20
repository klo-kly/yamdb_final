# Проект YaMDb

## Описание проекта
Проект YaMDb собирает отзывы `Review` пользователей на произведения `Titles`. Произведения делятся на категории: _«Книги», «Фильмы», «Музыка»_. Список категорий `Category` может быть расширен администратором (например, можно добавить категорию _«Изобразительное искусство»_ или _«Ювелирка»_). 

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: _книги, фильмы или музыка_. Например, в категории _«Книги»_ могут быть произведения _«Винни-Пух и все-все-все»_ и _«Марсианские хроники»_, а в категории _«Музыка»_ — _песня «Давеча» группы «Насекомые» и вторая сюита Баха_.
Произведению может быть присвоен жанр `Genre` из списка предустановленных (_например, «Сказка», «Рок» или «Артхаус»_). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы `Review` и ставят произведению оценку в диапазоне от одного до десяти _(целое число)_; из пользовательских оценок формируется усреднённая оценка произведения — _рейтинг (целое число)_. На одно произведение пользователь может оставить только один отзыв.


## Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (`user`) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (_фильмам/книгам/песенкам_), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (`moderator`) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django (`superuser`) должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Ресурсы API YaMDb
- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (_определённый фильм, книга или песенка_).
- Ресурс `categories`: категории (типы) произведений (_«Фильмы», «Книги», «Музыка»_).
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.

 Каждый ресурс описан в документации: указаны эндпоинты (_адреса, по которым можно сделать запрос_), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.
Полный список методов представлен по адресу http://localhost:8000/redoc/



## Установка
Клонируем репозиторий.
```sh
$ git clone https://github.com/github_username/api_yamdb.git
```
Создаем и активируем виртуальное окружение.
```sh
$ python -m venv venv
$ source venv/scripts/activate
```
Устанавливаем зависимости.
```sh
$ pip install -r requirements.txt
```
Создаем и применяем миграции.
```sh
$ python manage.py makemigrations 
$ python manage.py migrate
```
Запускаем локальный сервер.
```sh
$ python manage.py runserver
```
Адрес локального сервера:
```sh
127.0.0.1:8000
```

## Шаблон наполнения env-файла
```sh
DB_ENGINE=<указываем,базу данных с которой работаем>
DB_NAME=<имя базы данных>
POSTGRES_USER=<логин для подключения к базе данных>
POSTGRES_PASSWORD=<пароль для подключения к БД>
DB_HOST=<название сервиса (контейнера)>
DB_PORT=<порт для подключения к БД>
```
## Примеры

Для формирования запросов будет использована программа `Postman`.
- [Регистрация новых пользователей](api_yamdb/static/pictures/readme/signup.jpg)

- [Получение токена для аутентификации](api_yamdb/static/pictures/readme/token.jpg)

- [Получение списка отзывов](api_yamdb/static/pictures/readme/get_reviews.jpg)

- [Создание нового отзыва](api_yamdb/static/pictures/readme/post_reviews.jpg)


## Команды для запуска приложения в Docker контейнерах
Собираем образ(команда выполняется из директории, где сохранен Dockerfile)
```sh 
docker build -t <название образа> .
```

Запускаем контейнер
```sh 
docker run --name <имя контейнера> -it -p 8000:8000 yamdb
```
## Команда для наполнения базы данными
fixtures.json - это дамп с начальными данными
```sh 
python manage.py loaddata fixtures.json
```
![workwlof point](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)

Приложение развернуто на сервере: http://51.250.30.245/admin/
**Приятного использования**
