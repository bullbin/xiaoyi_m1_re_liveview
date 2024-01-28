from enum import Enum
from typing import Dict
from .const_http_cmd_rc_params import *

class CmdEnumFileQuality(str, Enum):
    Best = "Original"
    Medium = "MidThumb"
    Fast = "Thumbnail"

class CmdJsonDecoding(str, Enum):
    ExposureMode = "ExposureMode",
    MeteringMode = "MeteringMode",
    ImageQuality = "ImageQuality",
    ImageAspect = "ImageAspect",
    DriveMode = "DriveMode",
    FileFormat = "FileFormat",
    FStop = "Fnumber",
    FStopMin = "FnumberMin",
    FStopMax = "FnumberMax",
    ShutterSpeed = "ShutterSpeed",
    WhiteBalance = "WB",
    EvOffset = "EV",
    IsoSetting = "ISOSetting",
    IsoSettingAuto = "ISOAutoValue",
    ColorStyle = "ColorMode",
    LensStatus = "LensStatus",
    FocusMode = "FocusMode"

MAP_JSON_TO_ENUM : Dict[Enum, Enum] = {
    CmdJsonDecoding.ExposureMode : RcExposureMode,
    CmdJsonDecoding.MeteringMode : RcMeteringMode,
    CmdJsonDecoding.ImageQuality : RcImageQuality,
    CmdJsonDecoding.ImageAspect : RcImageAspect,
    CmdJsonDecoding.DriveMode : RcDriveMode,
    CmdJsonDecoding.FileFormat : RcFileFormat,
    CmdJsonDecoding.FStop : RcFStop,
    CmdJsonDecoding.FStopMin : RcFStop,
    CmdJsonDecoding.FStopMax : RcFStop,
    CmdJsonDecoding.ShutterSpeed : RcShutterSpeed,
    CmdJsonDecoding.WhiteBalance : RcWhiteBalance,
    CmdJsonDecoding.EvOffset : RcEvOffset,
    CmdJsonDecoding.IsoSetting : RcIso,
    CmdJsonDecoding.IsoSettingAuto : RcIso,
    CmdJsonDecoding.ColorStyle : RcColorStyle,
    CmdJsonDecoding.LensStatus : RcLensStatus,
    CmdJsonDecoding.FocusMode : RcFocusMode
}