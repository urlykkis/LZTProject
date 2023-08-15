import os
import logging
from logging import Logger


def setup_logger(
        file_name: str,
        level=logging.DEBUG,
        log_folder: str = 'logs'
) -> Logger:
    """
    Создает логгер

    :param file_name: Название логгера
    :type level: Уровень логгера
    :param log_folder: Папка для хранения файлов логов
    """

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, file_name + '.log')

    logger = logging.getLogger(file_name)
    logger.setLevel(level)

    # Настраиваем вывод | Время - Уровень - Название логгера - Сообщение
    formatter = logging.Formatter(
        u'%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler()  # Обработчик для консоли
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
