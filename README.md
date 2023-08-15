# LZT Project

# ТЗ
Написать на selenium/playwright скрипт, который будет входить на ютуб по куки, искать в строке поиска любой запрос, заходить по 6-ому видео, ставить лайк и подписываться на канал.


# Установка

Рекомендуемая версия: Python 3.11

## Windows
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Linux
```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


# Использование

Установить Python, venv, зависимости
Создать в папке со скриптом папку cookies и загрузить туда куки в .txt формате  
Формат куки - ```domain    TRUE    path    secure  Expires     Name    Value  ```

Запустить скрипт:
```python main.py```


После использования - 
```deactivate```