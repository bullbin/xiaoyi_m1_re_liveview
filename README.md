# Xiaoyi Yi M1 Camera Wireless Protocol Reverse Engineering
The Yi M1 was Xiaoyi's first (and last) attempt at a sleek and modern M4/3 camera. While it never received the support it needed to iron out the remaining quirks of the firmware, the final package produces great images and can be found very cheap on the second-hand market. Along with updates, Yi released a now-abandoned app for remote control of the camera; unfortunately, this is long outdated and increasingly harder to run. Since my usage of the camera needs this feature, I ended up looking into the protocols required to replicate the Yi Mirrorless app functionality; this repo contains a proof-of-concept for triggering a connection handshake with the camera over Bluetooth and decoding the live view feed returned.

## How does communication work?
The Yi M1 uses two methods of communication: Bluetooth Low Energy and Wi-Fi 801.11n with WPA2 encryption. BLE is used to find and negotiate a connection with the camera before Wi-Fi can be activated.

### BLE Protocol Characteristic UUIDs
BLE traffic is very barebones. All communication is entirely plaintext. The following summarises communication with the camera, but if you want specifics read `ble_keyhack.py`.
- Read ``41106da2-25ad-477b-a884-5038b6de4649`` for firmware information. This includes firmware versions for both the body and attached lens and tells Yi Mirrorless whether the camera is a Chinese or global model.
- Write ``41106da0-25ad-477b-a884-5038b6de4649`` to pair to the camera. Pairing operates by sending a key between 0 - 99998 (inclusive) which the camera will associate with the connected device. This will trigger a pairing request on the camera screen.
- Notify ``41106da7-25ad-477b-a884-5038b6de4649`` for when the camera has handled the pairing request. Returned data will be either a token or empty if the request was denied. The token is required to connect to the camera; if the token is already known, there is no need to re-pair to the camera.
- Write `41106da4-25ad-477b-a884-5038b6de4649` to begin a BLE control session on the camera. The message will contain the negotiated token, a  protocol version and a checksum. If this is valid, the camera will allow access to protected characteristics to complete control hand-off.
- Write `41106da5-25ad-477b-a884-5038b6de4649` to toggle Wi-Fi on the camera. This is protected and requires the session to be authenticated successfully.
- Read `41106da6-25ad-477b-a884-5038b6de4649` to get the SSID and passkey for the Wi-Fi network on the camera. This is protected and requires the session to be authenticated successfully. The network itself has a randomized 8-digit key so this information must be retained for each new session.

There are some services skipped for brevity and not all services are implemented (for example, we do not sync time with the camera as it is not required). As we could not decompile the camera firmware without artifacts, not all information is understood but the above is about all the capabilities the camera offers exposes while in BLE mode. BLE is strictly for negotiating credentials for the onboard wireless network where more complex operations can be completed.

We offer demo implementation ``debug_ble.py`` that will pair to the closest camera, authenticate the connection, activate Wi-Fi and return the SSID and passkey. Because the camera only supports one pairing key at a time, this will overwrite any prior connection to the app so you will need to re-pair if re-using Yi Mirrorless.

### Wi-Fi Communication Protocol
When Wi-Fi is active, the camera holds IP address 192.168.0.10 and will only assign an IP address to the first connected device - in other words, the network itself is for strictly one-to-one communication. Communication is completed entirely through GET requests to the URL http://192.168.0.10; [Qgrade](https://github.com/Qgrade/Yi-M1-mirrorless) covers this well in their work in finding camera commands. All command strings and their encoded parameters from Yi Mirrorless are included in ``const_http_cmd.py`` and ``const_http_cmd_rc_params.py`` respectively.

Remote control is triggered by calling command ``RCStartRemoteCtl``;  ``debug_html.py`` can be used to do this. In this mode, commands can be sent to adjust camera parameters and the camera will broadcast a live feed of the electronic preview through UDP port 54321 (which is shared with other Yi Home devices). For each preview frame, the camera encodes its own settings in plaintext alongside an 800x600 JPEG rendition of the live view; we include the means to decode this in ``udp_bitmap_decoder.py``. As traffic is heavy while remote control is active, there is a slight lag between sending commands and the camera processing them; do not assume the camera has responded to a command until the returned preview frame shows the settings have been changed successfully.

Unfortunately, because the camera only has an electronic viewfinder and not a true live view, remote control isn't any more capable for previewing settings. Processing happens on-camera so we can't do anything else with the provided video feed. There isn't any extra functionality exposed through this protocol.

## How was this research sourced?
Research was completed using hints from decompiling and traffic capture. More specifically, we used the following:
 - Decompilation of Yi Mirrorless 3.1.6 for Android
 - Bluetooth and Wi-Fi packet dumps while controlling the camera using the Yi Mirrorless app
 
 We only claim the research to be functional on firmware 3.2int of the camera (the last released firmware). The app negotiates communication based on the firmware version of the camera and there appears to be differences in the protocols used. We implement the final version of both protocols (BLE protocol 1.0 and WLAN protocol for firmwares >= 2.2); as firmware decompilation seems slightly broken and no custom firmware flashing routine is available, we will not support earlier software. It is recommended you update your camera to latest firmware to ensure compatibility as protocol faults can cause the camera to hard crash and restart. **Don't worry, you can't break your camera doing this.** We recommend against using the firmware upload commands; [protyposis](https://github.com/protyposis/yi-mirrorless-firmware-tools) has tools to pack custom firmware but warns against their usage.
 
## How do I run this?
For now, we include a simple library contained in ``prot_ble`` and ``prot_html`` that encompasses all known communication UUIDs and commands. We do not implement callable versions of many of the HTML commands; while they are self-explanatory, we recommend reading [Qgrade's](https://github.com/Qgrade/Yi-M1-mirrorless) work for manually triggering operations on the camera. To trigger our proof-of-concept, do the following:

1. Install requirements by doing ``pip install -r requirements.txt``
   - If needed, update your camera to firmware 3.2int
2. Turn on Bluetooth on your machine. Your computer **must** support Bluetooth Low Energy or communication will fail
3. Turn on your camera; disconnect from the app if active
4. Run ``debug_ble.py``; press Accept on the camera. If successful, the SSID and passkey will be returned. Try again if this fails, Bluetooth connections aren't always immediate and there is Bluetooth lag on the camera
5. Connect to the Wi-Fi network using the provided credentials. Since the password changes between sessions, you may need to forget the camera's network on your computer (this is required on Windows)
   - If prompted, allow Python to access the network
   - If you have any VPN active, you may need to disable it while accessing the camera
6. Run ``debug_html.py`` to start live view streaming on the camera
7. Run ``udp_bitmap_decoder.py`` to start dumping the live view feed and parameters. **This spawns images very quickly, don't run this for long!**

To stop live view, stop the connection on the camera or edit ``debug_html.py`` to broadcast ``RcCmdStop``. Dumped frames contain both a JPEG component and a text file; parameters correspond to ``const_http_cmd_rc_params.py`` but we don't provide a means to decode them (yet!)

**Have any problems?** Please open a GitHub issue! Don't forget to include your camera firmware and the error message - thanks in advance.

## What next?
With the Bluetooth protocol and UDP stream decoding now having successful open-source implementations, this covers all that is needed to create a complete replacement for the Yi Mirrorless app.  I hope to work on this when I get some free time!

## Credits (and thanks)
- [protyposis](https://github.com/protyposis/yi-mirrorless-firmware-tools) for their information on the HTTP server and getting this project started
- [Qgrade](https://github.com/Qgrade/Yi-M1-mirrorless) for their work on documenting camera commands
- Contributors of [JADX](https://github.com/skylot/jadx) for making Yi Mirrorless decompiling painless!
- Contributors of [PCAPdroid](https://github.com/emanuele-f/PCAPdroid) for helping dump HTTP packets
- Contributors of [Wireshark](https://www.wireshark.org/) for helping read BLE packet dumps (but no thanks for Android making BLE dumps annoying to take)
- Developers of Yi Mirrorless for not obfuscating the code in any way 😁
