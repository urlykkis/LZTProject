from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from .logger import setup_logger

logger = setup_logger('interactions')


def login_youtube(cookies: list[dict], youtube_url: str) -> WebDriver:
    """
    Создает браузер с куками и переходит по ссылке ютуб

    :param cookies : Лист с {name, value, path, expires, domain} куками,
    :param youtube_url : Ссылка на ютуб
    """

    chrome_service = ChromeService()
    chrome_options = Options()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get(youtube_url)

    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            logger.debug(f"Invalid Cookie: {cookie}")

    driver.refresh()

    return driver


def is_logged_in(driver) -> bool:
    """
    Проверяет вошло ли в аккаунт

    :param driver : Браузер
    :returns: True Если вошло в аккаунт | False Если не вошел в аккаунт (куки мертвы, не смог дождаться загрузки)
    """

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "avatar-btn"))
        )
        logger.info("Вошел по кукам")
        return True

    except TimeoutException:
        logger.info("Куки мертвы или скрипт не смог дождаться загрузки.")
        return False


def find_sixth_video(driver) -> bool:
    """
    Находит 6-о видео на странице поиска видео

    :param driver: Браузер
    :returns: True Если нашел видео и перешел на него | False Если не нашел 6-ое видео
    """

    video_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             "ytd-video-renderer:not([short-byline]) #video-title"))
    )[:6]

    if len(video_elements) == 6:
        video_elements[5].click()
        return True

    logger.warning("Меньше 6 видео найдено на странице.")
    return False


def like_and_subscribe(driver) -> None:
    """
    Лайкает видео и подписывается на канал

    :param driver: Браузер
    """
    try:
        # Ждем пока загрузиться кнопка лайка
        like_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button')
            )
        )

        if like_button.get_attribute("aria-pressed") == "false":  # Проверка что лайк уже поставлен
            like_button.click()
            logger.info("Лайк поставлен")
        else:
            logger.info("Лайк уже стоит на видео")

    except TimeoutException:
        logger.error("Таймаут при ожидании кнопки лайка.")

    try:
        # Ждем пока загрузиться кнопка подписки.
        subscribe_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@id="subscribe-button-shape"]/button'))
        )
        if not subscribe_button.is_displayed():  # Проверяем, что кнопка серая (не показывается)
            logger.info("Уже подписан на канал.")
        else:
            is_hidden_button = subscribe_button.get_attribute('hidden')

            if is_hidden_button == 'true':
                logger.info("Уже подписан на канал.")
            else:
                subscribe_button.click()
                logger.info("Подписался на канал.")

    except TimeoutException:
        logger.error("Таймаут при ожидании загрузки кнопки подписки.")


def channel_search_and_transition(
        driver,
        query: str = "Видео с длиной 1 секундой"
) -> bool:
    """
    Ищет в поиске видео с заданным запросом

    :param driver: Браузер
    :param query: Запрос для видео
    :returns: True если смог начать поиск видео | False если не смог начать
    """

    try:
        search_box = driver.find_element(By.NAME, "search_query")
        search_query = query
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        logger.info("Начал поиск видео")
        return True

    except:
        logger.info("Не смог начать поиск видео.")
        return False


def wait_video_load(driver) -> bool:
    """
    Ожидание загрузки видео

    :param driver: Браузер
    :returns: True если видео загрузилось | False если не загрузилось
    """
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".ytp-time-duration"))
        )

        logger.info("Видео загрузилось")
        return True
    except TimeoutException:
        logger.info("Видео не загрузилось")
        return False


def wait_search_results_load(driver) -> bool:
    """
    Ожидание загрузки страницы поиска

    :param driver: Браузер
    :returns: True если страница поиска загрузилось | False если не загрузилось
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )

        logger.info("Страница поиска загружена.")
        return True

    except TimeoutException:
        logger.info("Страница поиска не загрузилась.")
        return False
