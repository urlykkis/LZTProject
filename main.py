import os

from selenium.webdriver.remote.webdriver import WebDriver

from helpers import cookies as cookie_helper
from helpers import interactions, logger


logger = logger.setup_logger('main')


def process_cookie(
        cookie: list[dict],
        youtube_url: str = 'https://www.youtube.com'
) -> None:
    """
    Обработка куки, вход в аккаунт, проверка на вход, поиск по запросу, находит 6-ое видео, ставит лайк и подписку

    :param cookie: list[dict] : Список {name, value, expires, path, domain} куки
    :param youtube_url: str :  Ссылка на ютуб
    """

    try:
        # Загрузка куки и вход на YouTube
        driver: WebDriver = interactions.login_youtube(cookie, youtube_url)

        # Проверка на вход в аккаунт
        if interactions.is_logged_in(driver):
            # Поиск канала и переход
            if interactions.channel_search_and_transition(driver):
                # Ожидание загрузки результатов поиска
                if interactions.wait_search_results_load(driver):
                    # Поиск и переход к шестому видео
                    if interactions.find_sixth_video(driver):
                        # Ожидание загрузки видео
                        if interactions.wait_video_load(driver):
                            # Лайк и подписка
                            interactions.like_and_subscribe(driver)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

    finally:
        if 'driver' in locals():
            driver.quit()


def main(cookie_folder_path: str = './cookies/') -> None:
    """
    Основная функция

    :param cookie_folder_path: Путь до папки куки
    """

    logger.info('Запуск скрипта')

    if not os.path.exists(cookie_folder_path):
        logger.error(f"Папка {cookie_folder_path} не существует.\n"
                     f"Создайте папку cookies в папке со скриптом")
        return

    cookies = cookie_helper.get_cookies(cookie_folder_path)  # Получает куки

    for cookie in cookies:
        if cookie:
            process_cookie(cookie)  # Обработка куки


if __name__ == '__main__':
    main()
