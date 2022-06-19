from typing import List
import logging
import time
import warnings

warnings.simplefilter("always")

# Import warning
warning = f" Test import warning"
warnings.warn(warning, ImportWarning)

log_date = str(time.strftime("%d-%m-%y_%H:%M:%S"))
log_name = f"logs/testlog_{log_date}.log"
logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG)

logging.info('test')

logging.warning('test1')


logging.info('test2')

test3 = (f"Graph properties changed. New properties are:\n"
        f"reflexive:     {True}\n"
        f"symmetric:     {False}\n"
        f"transitive:    {True}")

logging.info(test3)
date = time.strftime("%d-%m-%y_%H:%M:%S")
print(date)

def time_flag():
    return str(time.strftime("%d-%m-%y_%H:%M:%S"))

def f(val):
        it = None
        if val == True:
                warning = f" ({time_flag()}) RuntimeWarning - should show"
                warnings.warn(warning, RuntimeWarning)
                logging.warning(warning)
                return it
        return 5

a = f(True)

if not a:
        print("ok")
      
group = set()

a = True == False
print(a)
        