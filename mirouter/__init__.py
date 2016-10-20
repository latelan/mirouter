from mirouter import mirouter

__mirouter = mirouter()
def get_device_list(): return __mirouter.get_devlist()
