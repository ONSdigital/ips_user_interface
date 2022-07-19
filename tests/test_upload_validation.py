import time
import uuid

from ips_services.ips.util.services_logging import log

start_time = time.time()

# noinspection PyUnusedLocal
def setup_module(module):
    log.info("Module level start time: {}".format(start_time))

def test_all_empty_fail():
    pass

def test_half_empty_fail():
    pass

def test_all_preloaded_success():
    pass

def test_all_preloaded_save_continue_success():
    pass

def test_change_preloaded_success():
    pass

def test_change_preloaded_save_continue_success():
    pass


# noinspection PyUnusedLocal
def teardown_module(module):
    log.info("Duration: {}".format(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))))