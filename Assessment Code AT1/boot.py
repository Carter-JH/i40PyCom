import machine

from network import WLAN


#ssid and password of wireless router to connect to
wifi_ssid = 'Hardiman 2.4GHz'
wifi_pass = 'placeholder'

if machine.reset_cause() != machine.SOFT_RESET:
    # use station (client mode)    
    wlan = WLAN(mode=WLAN.STA)
    
    wlan.connect(wifi_ssid, auth=(WLAN.WPA2, wifi_pass), timeout=5000)

    while not wlan.isconnected(): 
         machine.idle()

print('Connected to wifi')
# display interface configuration
print(wlan.ifconfig())
machine.main('main.py')    # only needed in boot.py