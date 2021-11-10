Путь к базе данных задается в переменной DB_URI в файле config.py

**Создание базы данных**

*python -m database --create*


**Удаление базы данных**

*python -m database --drop*

**Ручное обновление цен на все товары пользователей**

*python -m database --price-update*


**Запуск автоматического обновления цен на все товары пользователей по расписанию**

Для работы автоматического необходимо установить и запустить redis

Вариант 1:

В одном терминале:

*celery -A tasks worker --loglevel=INFO -E*

Во втором терминале:

*celery -A tasks beat*

Вариант 2:

*celery -A tasks worker -B --loglevel=INFO -E*
