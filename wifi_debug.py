import winwifi

debug = winwifi.WinWiFi()
aps = debug.scan()

for ap in aps:
    print(ap.ssid)