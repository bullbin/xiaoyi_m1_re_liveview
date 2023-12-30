import asyncio
from bleak import BleakClient, BleakGATTCharacteristic, BleakScanner
from random import randint
from constants.const_ble_uuid import *
from typing import List
from zlib import crc32

def trim_byte_to_str(data : bytearray) -> str:
    return data.decode('ascii').rstrip('\x00')

class YiBleConnectProtocol():
    def __init__(self):
        self.__firmware_lens : str = ""
        self.__firmware_body : str = "M1"
        self.__is_global_variant : bool = False
        
        self.__ble_protocol : int = 0
        self.__ble_name = ""
        self.__ble_manufacturer = ""
        self.__ble_model_number = ""
        self.__ble_key : str = ""
        self.__ble_token : str = ""
        self.__ble_retrieve_successful = False
        self.__ble_key_negotiated = False
        self.__ble_session_started = False

        self.__wlanSsid = ""
        self.__wlanPwd = ""
        
        self.__state_awaiting_pair = False

    async def retrieve_info(self, client : BleakClient):

        def check_is_global_variant(variant : str, firmware : str) -> bool:
            
            def str_check_china(id : str) -> bool:
                return len(id) == 0 or id in ["M1CN", "M1"] or id != "M1INT"
            
            if len(variant) == 0:
                return not str_check_china(firmware)
            return not str_check_china(variant)

        if not(client.is_connected):
            return

        self.__ble_name         = trim_byte_to_str(await client.read_gatt_char(UUID_STD_DEVICE_NAME))
        self.__ble_manufacturer = trim_byte_to_str(await client.read_gatt_char(UUID_STD_DEVICE_MANUFACTURER))
        self.__ble_model_number = trim_byte_to_str(await client.read_gatt_char(UUID_STD_MODEL_NUMBER))

        firmware_info : List[str] = trim_byte_to_str(await client.read_gatt_char(UUID_CHAR_FIRMWARE_INFO)).split(",")
        if len(firmware_info) >= 3:
            if firmware_info[0].isdigit(): self.__ble_protocol = int(firmware_info[0])
            self.__firmware_body = firmware_info[1]
            self.__is_global_variant = check_is_global_variant(firmware_info[2], self.__firmware_body)

            if len(firmware_info) > 3:
                self.__firmware_lens = firmware_info[3]
        
            self.__ble_retrieve_successful = True
    
    def __debug_on_extra_notify(self, characteristic : BleakGATTCharacteristic, data : bytearray):
        print("Unhandled", characteristic.uuid, data)

    def __on_pair_action(self, _characteristic : BleakGATTCharacteristic, data : bytearray):
        token = trim_byte_to_str(data)
        
        if len(token) == 0:
            self.__state_awaiting_pair = False
            print("\tPairing request denied.")
            return

        self.__ble_token = token
        self.__ble_key_negotiated = True
        self.__state_awaiting_pair = False
        print("\tPairing completed, token %s generated with key %s. Starting session..." % (token, self.__ble_key))

    async def do_pairing(self, client : BleakClient) -> bool:
        if not(client.is_connected and self.__ble_retrieve_successful):
            return False

        print("Attempting key negotiation...")
        self.__ble_key = str(randint(0, 99998))
        params = "%d,%s,android" % (self.__ble_protocol, self.__ble_key)
        print("\tDispatching key. Please press Accept on the camera.")

        await client.start_notify(UUID_CHAR_PAIRING_NOTIF, self.__on_pair_action)
        await client.write_gatt_char(UUID_CHAR_PAIRING_INIT, params.encode('ascii'), response=True)

        self.__state_awaiting_pair = True

    async def do_session_start(self, client : BleakClient):
        response = "1" + self.__ble_key + self.__ble_token
        response = response.encode('ascii')
        checksum = crc32(response)
        params = "%d,%s,%d" % (self.__ble_protocol, self.__ble_key, checksum)
        await client.write_gatt_char(UUID_CHAR_START_SESSION, params.encode('ascii'), response=True)
    
    async def start_wifi_connect(self, client : BleakClient):
        wlan_credentials = trim_byte_to_str(await client.read_gatt_char(UUID_CHAR_WIFI_AP_KEYSHARE)).split(",")
        if len(wlan_credentials) == 2:
            self.__wlanSsid = wlan_credentials[0]
            self.__wlanPwd = wlan_credentials[1]
            await client.start_notify("41106daf-25ad-477b-a884-5038b6de4649", self.__debug_on_extra_notify)
            # TODO - f characteristic means write a 3 key, but wifi initialises anyways
            await client.start_notify("41106dae-25ad-477b-a884-5038b6de4649", self.__debug_on_extra_notify)

            print("Handshake authenticated. WLAN credentials extracted, SSID %s, passkey %s. Enabling Wi-Fi..." % (self.__wlanSsid, self.__wlanPwd))
            await client.write_gatt_char(UUID_CHAR_WIFI_SWITCH, "ON".encode('ascii'))

    def __str__(self):
        return ' '.join([str(self.__ble_protocol), self.__firmware_lens, self.__firmware_body, str(self.__is_global_variant), self.__ble_name, self.__ble_manufacturer, self.__ble_model_number])

    def busy(self):
        return self.__state_awaiting_pair
    
    def can_start_session(self):
        return self.__ble_key_negotiated and not(self.__ble_session_started)

async def get_mac_address_cameras() -> List[str]:
    scanner = BleakScanner(service_uuids=[UUID_SERVICE_M1])
    devices = await scanner.discover(return_adv=True)
    devices = [(d.address,a.rssi) for d,a in devices.values() if a.rssi >= -50]     # Filter on signal strength
    devices = sorted(devices, key=lambda x: x[1], reverse=True)   # Sort by signal strength, highest is better
    return [a for a,_r in devices]

async def main():

    addresses = await get_mac_address_cameras()

    if len(addresses) == 0:
        print("Camera not in range.")
        return
    else:
        print("Detected candidates", ", ".join(addresses) + ". Connecting to %s..." % addresses[0])

    async with BleakClient(addresses[0]) as client:
        debug = YiBleConnectProtocol()
        await debug.retrieve_info(client)
        await debug.do_pairing(client)
        while debug.busy():
            await asyncio.sleep(2.0)

        if debug.can_start_session():
            await debug.do_session_start(client)
            await debug.start_wifi_connect(client)

        await asyncio.sleep(8.0)
        

asyncio.run(main())