from time import sleep
from threading import Event, Thread

# Hardware-related hooks
import zerophone_hw
from pyric import pyw

# Local imports
from rpc_api import RPCApi
from sources import ThrottledSource

# API version, kind-of-semver
api_version = (0,0,1)

api = RPCApi({"rpc_port":9376, "rpc_host":"127.0.0.1"})


dcdc = zerophone_hw.USB_DCDC()
led = zerophone_hw.RGB_LED()

def register_with(api, aliases=[], name=None):
    def decorator(f):
        api.register_function(f, function_name=name, aliases=aliases)
        return f
    return decorator

@register_with(api, name="api_version")
def get_api_version():
    return api_version

# USB DC-DC functions

@register_with(api)
def dcdc_state():
    return dcdc.gpio_state

@register_with(api)
def turn_dcdc_on():
    dcdc.on()
    return True

@register_with(api)
def turn_dcdc_off():
    dcdc.off()
    return True

""" Not sure if we need this kind of calling convention
@register_with(api)
def dcdc(state=None):
    if state is not None:
        return dcdc_state()
    else:
        if state:
            return turn_dcdc_on()
        else:
            return turn_dcdc_off()
"""

# WiFi functions

def get_wif_from_wifs(wifs):
    return wifs[0] # *very* simple heuristic =D

def pyw_link_info():
    wifs = pyw.winterfaces()
    if not wifs:
        return None
    wif = get_wif_from_wifs(wifs)
    c = pyw.getcard(wif)
    info = pyw.link(c)
    info["card"] = wif
    return info

wifi_info_source = ThrottledSource(pyw_link_info, 3)

@register_with(api)
def wifi_connected():
    info = wifi_info_source.get()
    if not info:
        return None
    return info.get("stat", None) == 'associated'

@register_with(api)
def wifi_info():
    info = wifi_info_source.get()
    if not info:
        return None
    return info

@register_with(api)
def wifi_strength():
    info = wifi_info_source.get()
    if not info:
        return None
    rss = info.get("rss", None)
    if rss is None:
        return None
    # Will change soon, for now, just monitoring the possible values.
    return rss

@register_with(api)
def wifi_ssid():
    info = wifi_info_source.get()
    if not info:
        return None
    return info.get("ssid", None)

@register_with(api)
def wifi_bssid():
    info = wifi_info_source.get()
    if not info:
        return None
    return info.get("bssid", None)

""" Not implemented in software yet

@register_with(api)
def wifi_powered():
    return True

@register_with(api)
def turn_wifi_on():
    return True

@register_with(api)
def turn_wifi_off():
    return False

"""

# LED functions

@register_with(api)
def set_led_color(color_str):
    return led.set_color(color_str)

@register_with(api)
def set_led_rgb(r, g, b):
    return led.set_rgb(r, g, b)

# Charger functions

@register_with(api)
def charger_connected():
    return zerophone_hw.is_charging()

""" Not implemented in software yet

# Battery functions

@register_with(api)
def battery_level():
    return 100

# GSM functions

@register_with(api)
def gsm_powered():
    return False

@register_with(api)
def start_gsm():
    modem.reset()
    return False

@register_with(api)
def stop_gsm():
    return False

@register_with(api)
def restart_gsm():
    result = stop_gsm()
    if not result:
        return False
    result = start_gsm()
    if not result:
        return False
    return True

@register_with(api)
def gsm_strength():
    return 20
"""

# The source polling API - is more efficient for sources that
# require resources for polling (i.e. requesting battery level
# from the GSM modem using AT commands). If there's anywhere
# that we can save ourselves a couple of context switches and
# CPU time, it's by using this polling API (together with
# ThrottledSource and whatever else comes in the future).

#         "source_name":(callback,   throttle_level)
sources = {"dcdc_state":(dcdc_state, 1),
           #"gsm_running":gsm_running,
           #"gsm_strength":gsm_strength,
           "wifi_strength":(wifi_strength, 10),
           "wifi_connected":(wifi_connected, 10),
           "wifi_info":(wifi_info, 10),
           "wifi_ssid":(wifi_ssid, 10),
           "wifi_bssid":(wifi_bssid, 10),
           "charger_connected":(charger_connected, 10),
           #"battery_level":battery_level,
           }

source_values = {s:None for s in sources.keys()}

source_refcount = {s:0 for s in sources.keys()}

source_throttle = {s:0 for s in sources.keys()}

source_timeouts = {s:0 for s in sources.keys()}

requests = []

source_timeout = 200

@register_with(api)
def request_source_poll(keys):
    requests.append(keys)
    for k in keys:
        if k in source_refcount:
            source_refcount[k] += 1
            source_timeouts[k] = 0
        else: # Unknown source, but we won't just error out on it, that wouldn't be nice
            pass

@register_with(api, aliases=["get_polled_sources"])
def get_sources(keys):
    data = {}
    for k in keys:
        if k in source_timeouts.keys():
            source_timeouts[k] = 0
        if k not in sources.keys():
            v = "unavailable"
        elif source_refcount[k] == 0:
            v = "not polled"
        else:
            v = source_values.get(k, "unavailable")
        data[k] = v
    return data

@register_with(api)
def check_polled_sources(keys):
    polled_sources = list_polled_sources()
    return all([key in polled_sources for key in keys])

@register_with(api, aliases=["get_available_sources"])
def list_sources():
    return list(sources.keys())

@register_with(api)
def list_polled_sources():
    return [k for k,v in source_refcount.items() if v>0]

def polling_process():
    sources_to_poll = list_polled_sources()
    for source in sources_to_poll:
        #print(source)
        if source in sources.keys():
            #print("polling source {} - throttle {}".format(source, source_throttle[source]))
            if source_throttle[source] == sources[source][1]:
                print("polling source {}".format(source))
                source_values[source] = sources[source][0]()
                source_throttle[source] = 0
            else:
                source_throttle[source] += 1
        else:
            source_values[source] = "unrecognized source"

do_run_polling = Event()
sleep_time = 0.1

def polling_loop():
    do_run_polling.set()
    while do_run_polling.isSet():
        polling_process()
        for source, value in source_timeouts.items():
            if source_refcount[source] > 0:
                #print("{} - {}".format(source, value))
                if value >= source_timeout:
                    source_refcount[source] = 0
                source_timeouts[source] = value + 1
        sleep(sleep_time)

t = None

def run_polling():
   global t
   t = Thread(target=polling_loop)
   t.daemon = True
   t.start()

def main():
    api.start_thread()
    polling_loop()

if __name__ == "__main__":
    api.start_thread()
    #polling_loop()
    run_polling()
