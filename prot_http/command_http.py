from __future__ import annotations
from .const_http_cmd import YiHttpCmdId
from .const_http_cmd_rc_params import *
from .const_http_enum_extra import *
from typing import Dict, List

class YiHttpCmd():
    @staticmethod
    def from_json(json : str) -> YiHttpCmd:
        raise NotImplementedError
    
    def to_json(self) -> Dict[str,str]:
        raise NotImplementedError

class CmdFileList(YiHttpCmd):
    def __init__(self, permit_raw : bool = False, permit_jpg : bool = False, id_start : int = 0, id_end : int = 0):
        """List images on camera.

        Args:
            permit_raw (bool, optional): Allow DNG images. Defaults to False.
            permit_jpg (bool, optional): Allow JPEG images. Defaults to False.
            id_start (int, optional): Index of starting image. Defaults to 0.
            id_end (int, optional): Index of ending image. Defaults to 0.
        """
        super().__init__()
        self.__filetype : str = "all"
        if permit_raw:
            if not(permit_jpg):
                self.__filetype : str = "DNG"
        elif permit_jpg:
            self.__filetype : str = "JPG"
        
        self.__range_start : int = max(id_start, 0)
        self.__range_end : int = max(id_end, self.__range_start)

    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_FILE_LIST.value, "range_start":str(self.__range_start),
                "range_end":str(self.__range_end), "filetype":self.__filetype}

class CmdFileDelete(YiHttpCmd):
    def __init__(self, photo_paths : List[str]):
        super().__init__()
        self.__paths = photo_paths
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_FILE_DELETE.value, "file_list":self.__paths}

class CmdFileGet(YiHttpCmd):
    def __init__(self, path_file : str, quality : CmdEnumFileQuality):
        super().__init__()
        self.__path = path_file
        self.__quality = quality
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_FILE_GET.value, "path":self.__path, "resulotion":self.__quality.value}

class CmdLiveViewStart(YiHttpCmd):
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_LIVE_VIEW_START.value}

class RcCmdSetCameraMode(YiHttpCmd):
    def __init__(self, mode : RcExposureMode):
        """Change camera mode.

        Args:
            mode (RcExposureMode): New mode dial setting.
        """
        super().__init__()
        self.__mode = mode

    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_EXPOSURE_MODE.value, "DialMode":self.__mode.value}

class RcCmdSetMeteringMode(YiHttpCmd):
    def __init__(self, mode : RcMeteringMode):
        super().__init__()
        self.__mode = mode
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_METERING_MODE.value, "MeteringMode":self.__mode.value}

class RcCmdSetFocusingMode(YiHttpCmd):
    def __init__(self, mode : RcFocusMode):
        super().__init__()
        self.__mode = mode
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_FOCUS_MODE.value, "FocusMode":self.__mode.value}

class RcCmdSetImageQuality(YiHttpCmd):
    def __init__(self, quality : RcImageQuality):
        super().__init__()
        self.__quality = quality
    
    def to_json(self) -> Dict[str,str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_IMAGE_QUALITY.value, "ImageQuality":self.__quality.value}

class RcCmdSetImageAspect(YiHttpCmd):
    def __init__(self, aspect : RcImageAspect):
        super().__init__()
        self.__aspect = aspect
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_IMAGE_ASPECT.value, "ImageAspect":self.__aspect.value}

class RcCmdSetImageFormat(YiHttpCmd):
    def __init__(self, file_format : RcFileFormat):
        super().__init__()
        self.__file_format = file_format
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_IMAGE_FORMAT.value, "FileFormat":self.__file_format.value}

class RcCmdSetDriveMode(YiHttpCmd):
    def __init__(self, drive_mode : RcDriveMode):
        super().__init__()
        self.__drive_mode = drive_mode
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_DRIVE_MODE.value, "DriveMode":self.__drive_mode.value}

class RcCmdSetFStop(YiHttpCmd):
    def __init__(self, f_stop : RcFStop):
        super().__init__()
        self.__f_stop = f_stop
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_FNUMBER.value, "Fnumber":self.__f_stop.value}

class RcCmdSetShutterSpeed(YiHttpCmd):
    def __init__(self, shutter_speed : RcShutterSpeed):
        super().__init__()
        self.__shutter_speed = shutter_speed
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_SHUTTER_SPEED.value, "ShutterSpeed":self.__shutter_speed.value}

class RcCmdSetExposureValueOffset(YiHttpCmd):
    def __init__(self, ev_offset : RcEvOffset):
        super().__init__()
        self.__ev_offset = ev_offset
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_EV.value, "EV":self.__ev_offset.value}

class RcCmdSetColorStyle(YiHttpCmd):
    def __init__(self, tone : RcColorStyle):
        super().__init__()
        self.__style = tone
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_COLOR_MODE.value, "ColorMode":self.__style.value}

class RcCmdSetWhiteBalanceMode(YiHttpCmd):
    def __init__(self, wb : RcWhiteBalance):
        super().__init__()
        self.__balance = wb
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_WB.value, "WB":self.__balance.value}

class RcCmdSetIso(YiHttpCmd):
    def __init__(self, iso : RcIso):
        super().__init__()
        self.__iso = iso
    
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SET_ISO.value, "ISO":self.__iso.value}

class RcCmdShootPhoto(YiHttpCmd):
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_SHOOT.value}

class RcCmdStart(YiHttpCmd):
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_START.value}

class RcCmdStop(YiHttpCmd):
    def to_json(self) -> Dict[str, str]:
        return {"command":YiHttpCmdId.CMD_RC_STOP.value}