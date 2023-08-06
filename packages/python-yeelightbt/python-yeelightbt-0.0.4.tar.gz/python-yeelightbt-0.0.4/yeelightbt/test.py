from yeelightbt import Lamp
mac = "f8:24:41:e7:8a:6f"
def notification_cb(x):
    pass

def paired_cb(x):
    pass


#lamp = Lamp(mac, notification_cb, paired_cb, keep_connection=True, wait_after_call=0.2)
#lamp.connect()
#x = yield from lamp.async_state()

def start_counting(x):
    import time
    time.sleep(1)
    x("result")

async def wait_and_return(cb):
    x = start_counting(cb)