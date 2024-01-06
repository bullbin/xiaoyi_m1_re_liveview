from prot_ble import trigger_remote_control_closest

ssid, pwd = trigger_remote_control_closest()
print("SSID\t%s\nPass\t%s" % (ssid, pwd))