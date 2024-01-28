# Translation layer for control of the Yi M1 like an OpenCV VideoCapture device
from typing import Optional, Tuple, Deque, Callable, Dict
from collections import deque
import cv2, time, socket, threading
import numpy as np

from prot_http.command_http import RcCmdStart, RcCmdStop, YiHttpCmd
from prot_ble.ble_keyhack import YiBleConnectProtocol

from urllib3 import PoolManager, HTTPResponse
from urllib3.exceptions import TimeoutError

from prot_http.const_http_enum_extra import *
from enum import Enum

from prot_http.const_wifi import *

YI_MAX_RESEND_HTTP : int = 5
YI_POLL_TIME : float = 0.1
YI_PREVIEW_WIDTH : int = 800
YI_PREVIEW_HEIGHT : int = 600
YI_TIMEOUT_DURATION : float = 1.0
YI_FRAME_WAIT_PERIOD : float = 0.001

class YiWebcamAfMode(Enum):
    RcFocusMode.ManualFocus = 0
    RcFocusMode.AutofocusContinuous = 1
    RcFocusMode.AutofocusStatic = 2

def null_cmd_handler(data : bytearray):
    pass

class YiM1_OpenCv_Webcam_VideoCapture():

    def __init__(self, queue_cam : Deque[Tuple[YiHttpCmd, Callable[[bytearray], None]]]):
        self.__lock_frame : threading.Lock = threading.Lock()
        self.__frame : Optional[np.ndarray] = None
        self.__frame_awaiting_next : bool = True

        self.__queue_cam : Deque[Tuple[YiHttpCmd, Callable[[bytearray], None]]] = queue_cam

        self.__current_idx_frame    : float     = 0.0
        self.__current_f            : float     = 0.0
        self.__current_iso          : float     = 100.0
        self.__current_e            : float     = 0.0
        self.__current_focus_mode   : RcFocusMode       = RcFocusMode.AutofocusContinuous
        self.__current_wb_mode      : RcWhiteBalance    = RcWhiteBalance.Auto

    def get(self, cv_prop : int) -> float:
        if cv_prop == cv2.CAP_PROP_POS_FRAMES:
            return self.__current_idx_frame
        
        elif cv_prop == cv2.CAP_PROP_FRAME_WIDTH:
            return float(YI_PREVIEW_WIDTH)
        elif cv_prop == cv2.CAP_PROP_FRAME_HEIGHT:
            return float(YI_PREVIEW_HEIGHT)
        
        elif cv_prop == cv2.CAP_PROP_FRAME_COUNT:
            return 30.0 # TODO - Is this correct?
        elif cv_prop == cv2.CAP_PROP_MODE:
            return cv2.CAP_MODE_BGR
        
        elif cv_prop == cv2.CAP_PROP_BRIGHTNESS or cv_prop == cv2.CAP_PROP_CONTRAST or cv_prop == cv2.CAP_PROP_SATURATION or cv_prop == cv2.CAP_PROP_HUE:
            return 0.0
        
        elif cv_prop == cv2.CAP_PROP_EXPOSURE:
            return self.__current_e
        
        elif cv_prop == cv2.CAP_PROP_CONVERT_RGB:
            return 1.0
        elif cv_prop == cv2.CAP_PROP_SHARPNESS:
            return 1.0
        elif cv_prop == cv2.CAP_PROP_AUTO_EXPOSURE:
            pass    # TODO
        
        elif cv_prop == cv2.CAP_PROP_GAMMA:
            return 100.0
        elif cv_prop == cv2.CAP_PROP_FOCUS:
            return 0.0      # TODO - Manual focus stops
        
        elif cv_prop == cv2.CAP_PROP_GUID:
            return 1.0
        elif cv_prop == cv2.CAP_PROP_ISO_SPEED:
            return self.__current_iso
        
        elif cv_prop == cv2.CAP_PROP_BACKLIGHT or cv_prop == cv2.CAP_PROP_PAN or cv_prop == cv2.CAP_PROP_TILT or cv_prop == cv2.CAP_PROP_ROLL:
            return 0.0

        elif cv_prop == cv2.CAP_PROP_IRIS:
            return self.__current_f
        elif cv_prop == cv2.CAP_PROP_BUFFERSIZE:
            return 1.0
        elif cv_prop == cv2.CAP_PROP_AUTOFOCUS:
            return float(YiWebcamAfMode[self.__current_focus_mode].value)
        elif cv_prop == cv2.CAP_PROP_BACKEND:
            return float(cv2.CAP_ANY)
        elif cv_prop == cv2.CAP_PROP_AUTO_WB:
            return float(self.__current_wb_mode == RcWhiteBalance.Auto)
        elif cv_prop == cv2.CAP_PROP_TEMPERATURE or cv_prop == cv2.CAP_PROP_WB_TEMPERATURE:
            if self.__current_wb_mode == RcWhiteBalance.Auto:
                return 0.0
            elif self.__current_wb_mode == RcWhiteBalance.Cloudy:
                return 6500.0
            elif self.__current_wb_mode == RcWhiteBalance.Incandescent:
                return 2600.0
            elif self.__current_wb_mode == RcWhiteBalance.Shadow:
                return 7150.0
            elif self.__current_wb_mode == RcWhiteBalance.Sunny:
                return 4000.0 # Not sure
            return float(self.__current_wb_mode == RcWhiteBalance.Auto)
        
        return -1.0
    
    def set(self, cv_prop : int) -> bool:
        return False

    def getBackendName()  -> str:
        return cv2.CAP_IMAGES

    def read(self) -> Tuple[bool, np.ndarray]:
        time_awaited = 0
        self.__frame_awaiting_next = True

        while self.__frame_awaiting_next and time_awaited < YI_TIMEOUT_DURATION:
            w_start = time.time()
            time.sleep(YI_FRAME_WAIT_PERIOD)
            time_awaited += time.time() - w_start
        
        with self.__lock_frame:
            frame_copy = np.copy(self.__frame)
        return not(self.__frame_awaiting_next), frame_copy
    
    def isOpened(self) -> bool:
        return True
    
    def update_params(self, f_idx : int, f : float, e : float, iso : float, mode_focus : RcFocusMode, mode_wb : RcWhiteBalance):
        self.__current_idx_frame = float(f_idx)
        self.__current_f = f
        self.__current_e = e
        self.__current_iso = iso
        self.__current_focus_mode = mode_focus
        self.__current_wb_mode = mode_wb

    def update_frame(self, frame : bytearray):

        def decode_memory_jpeg(jpeg_bytes : bytearray):
            with self.__lock_frame:
                self.__frame = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        jpg_decoder = threading.Thread(target=decode_memory_jpeg, args=[frame])
        jpg_decoder.start()

    def release(self):
        pass

class YiM1_OpenCv_Bridge():
    def __init__(self):
        self.__cmd_queue    : Deque[Tuple[YiHttpCmd, Callable[[bytearray], None]]]  = deque()
        self.__cv_cap       : YiM1_OpenCv_Webcam_VideoCapture                       = YiM1_OpenCv_Webcam_VideoCapture(self.__cmd_queue)

        self.__threading_udp_feedback : threading.Thread = threading.Thread(target=self.__on_frame_update, name="Yi UDP Receiver")
        self.__threading_cmd_feedback : threading.Thread = threading.Thread(target=self.__do_http_cmd, name="Yi HTTP Automator")

        self.__udp_alive = True
        self.__cmd_alive = True

        self.__socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__threading_cmd_feedback.start()

    # TODO - Halt until command delivered...
    def start_live_feed(self) -> YiM1_OpenCv_Webcam_VideoCapture:
        self.__socket_udp.bind(('', UDP_PORT_LIVEVIEW))
        self.__socket_udp.settimeout(2)
        self.__udp_alive = True
        self.__threading_udp_feedback.start()
        self.__cmd_queue.append((RcCmdStart(), null_cmd_handler))
        return self.__cv_cap

    def stop_live_feed(self):
        self.__udp_alive = False
        self.__cmd_queue.append((RcCmdStop(), null_cmd_handler))
        self.__threading_udp_feedback.join()
        self.__socket_udp.close()
    
    def __process_new_camera_frame(self, data : bytearray):
        self.__cv_cap.update_frame(data)
    
    def __process_new_camera_params(self, params : str, idx_frame : int):

        def header_to_params(header : str) -> Dict[Enum, Enum]:
            header = header.rstrip()
            
            if len(header) >= 2:
                header = header[1:-1]
                
            header = header.replace('"', '')
            header = header.split(",")

            param_dict : Dict[Enum, Enum] = {}
            for keypair in header:
                pair = keypair.split(":")
                if len(pair) != 2:
                    continue

                key, value = pair[0], pair[1]
                try:
                    key = CmdJsonDecoding(key)
                    val_map = MAP_JSON_TO_ENUM[key]
                    value = val_map(value)
                    param_dict[key] = value
                except ValueError:
                    pass
            
            return param_dict

        param_dict = header_to_params(params)

        e = 0.0
        f = 8.0
        iso = 100.0
        mode_focus = RcFocusMode.AutofocusContinuous
        mode_wb = RcWhiteBalance.Auto

        # TODO - Check auto mode
        if CmdJsonDecoding.IsoSetting in param_dict:
            if param_dict[CmdJsonDecoding.IsoSetting] == RcIso.Auto:
                if CmdJsonDecoding.IsoSettingAuto in param_dict:
                    iso = float(param_dict[CmdJsonDecoding.IsoSettingAuto].value)
            else:
                iso = float(param_dict[CmdJsonDecoding.IsoSetting].value)
        
        if CmdJsonDecoding.EvOffset in param_dict:
            e = float(param_dict[CmdJsonDecoding.EvOffset].value)

        if CmdJsonDecoding.WhiteBalance in param_dict:
            mode_wb = param_dict[CmdJsonDecoding.WhiteBalance]
        
        if CmdJsonDecoding.FocusMode in param_dict:
            mode_focus = param_dict[CmdJsonDecoding.FocusMode]
        
        if CmdJsonDecoding.FStop in param_dict:
            f = float(param_dict[CmdJsonDecoding.FStop].value)

        self.__cv_cap.update_params(idx_frame, f, e, iso, mode_focus, mode_wb)
    
    def __on_frame_update(self):
        data = bytearray(b'')
        data_idx_frame = None
        data_idx_last_packet = -1
        data_valid : bool = True

        while self.__udp_alive:
            try:
                pack, addr = self.__socket_udp.recvfrom(1024000)
                
                if len(pack) < 12:
                    continue

                idx_frame           = int.from_bytes(pack[:4], byteorder='big')
                len_packet_frame    = int.from_bytes(pack[4:8], byteorder='big')
                idx_packet_frame    = int.from_bytes(pack[8:12], byteorder='big')

                # If the reconstructed frame is not the delivered one, start reconstruction again
                if data_idx_frame != idx_frame:
                    data = bytearray(b'')
                    data_idx_frame = idx_frame
                    data_idx_last_packet = -1
                    data_valid = True
                
                if data_valid:
                    if (idx_packet_frame - 1) == data_idx_last_packet:
                        data.extend(pack[12:])
                        data_idx_last_packet = idx_packet_frame
                    else:
                        data_valid = False
                        continue

                    if (data_idx_last_packet == len_packet_frame - 1):
                        if len(data) > 2048:
                            self.__process_new_camera_params(data[:2048].decode('ascii'), idx_frame)
                            self.__process_new_camera_frame(data[2048:])

            except TimeoutError:
                print("Timeout on UDP, frame decoder stopped!")
                self.__udp_alive = False

    def __do_http_cmd(self):

        def get_response(http : PoolManager, cmd : YiHttpCmd) -> Optional[bytearray]:
            json = str(cmd.to_json()).replace("'", '"').replace(' "', '"')
            url = "http://%s/?data=%s" % (INET_ADDRESS_CAMERA, json)
            try:
                response : HTTPResponse = http.request("GET", url, timeout=1.0)
                return response.data
            except TimeoutError:
                return None
        
        count_resend : int = 0
        cmd_repeat  : Optional[YiHttpCmd] = None
        cmd_handler : Optional[Callable[[bytearray], None]] = None
        http = PoolManager()

        while self.__cmd_alive:
            if len(self.__cmd_queue) > 0 and cmd_repeat == None:
                cmd_repeat, cmd_handler = self.__cmd_queue.popleft()
                count_resend = 0
            
            if cmd_repeat != None:
                count_resend += 1
                response = get_response(http, cmd_repeat)
                if response != None:
                    cmd_handler(response)
                    
                    cmd_repeat = None
                    cmd_handler = None
                
                elif count_resend > YI_MAX_RESEND_HTTP:
                    raise TimeoutError("HTTP resent limit reached, Yi camera is not responding!")
                
            else:
                time.sleep(YI_POLL_TIME)