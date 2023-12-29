def connect_to_camera():
    pass

def is_ssid_camera(ssid : str) -> bool:
    return ssid.startswith(("\\YI_M1_", "YI_M1_"))

def camera_forget() -> bool:
    pass