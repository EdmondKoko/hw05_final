![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-2.2.6-red?style=for-the-badge&logo=django&logoColor=blue)
![SQLite](https://img.shields.io/badge/SQLite-grey?style=for-the-badge&logo=postgresql&logoColor=yellow)
![Pytest-django](https://img.shields.io/badge/pytest-django==3.8.0-orange?style=for-the-badge&logo=nginx&logoColor=green)


# Yatube - социальная сеть для публикации личных дневников. 

## Описание:
### Расширение проекта Yatube:

В проекте реализовано:
- Возможность регистрации и восстанавления доступа по электронной почте;
- Возможность добавить изображение к посту;
- Возможность создания и редактирования собственных записей;
- Возможность просмотривать страницы других авторов;
- Возможность комментировать записи других авторов;
- Возможность подписки и отписки от авторов;
- Возможность определить запись к отдельной группе;
- Личная страница публикации записей;
- Отдельная лента с постами авторов на которых подписан пользователь;
- Через панель администратора модерируются записи.

### Запуск приложения:

Клонируем проект:

```bash
git clone https://github.com/edmondkoko/yatube_v1.1_publications.git
```

Переходим в папку с проектом:

```bash
cd yatube_v1.1_publications
```

Устанавливаем виртуальное окружение:

```bash
python3 -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/bin/activate
```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Создаем супер пользователя:

```bash
python manage.py createsuperuser
```

Запускаем проект:

```bash
python manage.py runserver
```

После чего проект будет доступен по адресу (http://127.0.0.1:8000/)
