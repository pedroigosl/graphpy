from graph import start_log
import logging
import warnings
import time
# raise TypeError("wrong type")

# Warning configs
warnings.simplefilter("always")

# Import warning
warning = f" This library is a work in progress and not yet functional"
warnings.warn(warning, ImportWarning)

# Log configs
log_date = str(time.strftime("%d-%m-%y %H:%M:%S"))
log_name = f"logs/graphlog {log_date}.log"
print(f"Session log started at {log_name}")

# Warning configs
# warnings.simplefilter("always")


def start_log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%d-%m-%y %H:%M:%S",
                        filename=log_name,
                        filemode='w', level=logging.DEBUG)


def f(c):
    if c == 1:
        raise RuntimeError
    return True


start_log()
txt = f"{TypeError} test"
logging.error(txt)

time.sleep(1)
logging.error(txt)
warnings.warn("terst")
f(2)
print("h")
