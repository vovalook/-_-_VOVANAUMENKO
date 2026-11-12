# Практическая работа №9 — Django ORM
Индивидуальный проект «Удобрения для цветов», продолжение ПР5–ПР7. Исходный консольный проект предыдущих практик сохранён в корне репозитория. В каталоге PR9_Django_ORM содержится веб-версия с Django ORM.

## Выполнено
Модели Flower, Fertilizer, FertilizerFlower с отношением многие-ко-многим; миграция; ORM-запросы (17 самостоятельных примеров: получение, фильтрация, поиск, сортировка, связи, агрегаты, пагинация); Django-представления и существующие HTML-страницы. Включена загрузка первоначальных данных, соответствующих SQLite базе ПР7 (5 цветов, 5 удобрений, 11 связей).

## Запуск в VS Code (Windows, PowerShell)
Откройте папку PR9_Django_ORM как корень проекта:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py loaddata initial_data
.\.venv\Scripts\python.exe db\check_orm_examples.py
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

В браузере: http://127.0.0.1:8000/ и http://127.0.0.1:8000/fertilizer/1/.

## Перенос исходной базы ПР7
При наличии файла `fertilizers.sqlite3` в корне PR9_Django_ORM вместо `loaddata` можно выполнить `python db/import_sqlite_to_orm.py` после `migrate`. Исходная SQLite-база доступна в локальном архиве проекта, который был подготовлен для ПР9. GitHub содержит эквивалентный набор исходных записей в `fixtures/initial_data.json`.

## Что показать преподавателю
`fertilizers/models.py`, `migrations/0001_initial.py`, `fertilizers/orm_queries.py`, `fertilizers/views.py`, результат `showmigrations`, команды проверки, главную страницу и карточку удобрения.

**Проверка**: публикация в GitHub не означает, что Django был реально запущен; миграции и тесты должны быть проверены в вашей среде.
