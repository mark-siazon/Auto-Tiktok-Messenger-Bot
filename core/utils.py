import time
import random

def human_delay(min_sec=1, max_sec=3):
    # Sleep for a random duration to mimic human pauses
    time.sleep(random.uniform(min_sec, max_sec))

def type_like_human(element, text):
    # Type each character with a short random delay between keys
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
