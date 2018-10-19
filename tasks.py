from celery import Celery
import subprocess
import json
from selenium import webdriver
import time
from io import StringIO
from PIL import Image

celery = Celery("app", broker='redis://localhost:6379/0')
celery.conf.result_backend = 'redis://localhost:6379/0'
celery.conf.tasks_ack_late = True
celery.conf.worker_prefetch_multiplier = 1


@celery.task
def parse(website):
    process = subprocess.Popen(['lighthouse', '{}'.format(website), '--disable-device-emulation', '--disable-network-throttling', '--quiet', '--output=json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = process.communicate()[0]
    ret = process.wait()
    try:
        res = json.loads(output.decode('utf-8'))
    except Exception as e:
        res = e
    return res


@celery.task
def screen_shot(website):
    DRIVER = 'driver/chromedriver.exe'
    driver = webdriver.Chrome(DRIVER)
    driver.set_window_size(width=1360, height=800)
    driver.get(website)
    time.sleep(2)
    screenshot = driver.get_screenshot_as_base64()
    driver.quit()
    return screenshot