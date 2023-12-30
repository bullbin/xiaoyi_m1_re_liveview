from enum import Enum

class YiHttpCmdId(str, Enum):
    CMD_FILE_LIST               = "GetFileList"         # Done
    CMD_FILE_INFO               = "GetFileInfo"
    CMD_FILE_DELETE             = "DeleteFile"          # Done
    CMD_FILE_GET                = "GetFile"             # Done

    CMD_STATUS_CHECK            = "CheckPreUpdate"
    CMD_STATUS_GET              = "GetCameraStatus"

    CMD_FIRMWARE_UPLOAD_CAM     = "UpdateFW"
    CMD_FIRMWARE_UPLOAD_LENS    = "UpdateLenFW"
    
    CMD_MASTERGUIDE_LIST        = "GetMLFileList"
    CMD_MASTERGUIDE_INFO        = "GetMLFileInfo"
    CMD_MASTERGUIDE_DELETE      = "DeleteMLFile"
    CMD_MASTERGUIDE_UPLOAD      = "UploadML"

    CMD_LIVE_VIEW_START         = "StartLiveview"       # Done
    CMD_RC_START                = "RCStartRemoteCtl"    # Done
    CMD_RC_STOP                 = "RCStopRemoteCtl"     # Done

    CMD_RC_GET_CAMERA_CONFIG    = "RCGetCameraCfg"
    CMD_RC_SET_EXPOSURE_MODE    = "RCSwitchDialMode"    # Done
    CMD_RC_SET_METERING_MODE    = "RCMeteringModeSet"   # Done
    CMD_RC_SET_FOCUS_MODE       = "RCFocusModeSet"      # Done
    CMD_RC_SET_IMAGE_QUALITY    = "RCImageQualitySet"   # Done
    CMD_RC_SET_IMAGE_ASPECT     = "RCImageAspect"       # Done
    CMD_RC_SET_IMAGE_FORMAT     = "RCFileFormatSet"     # Done
    CMD_RC_SET_DRIVE_MODE       = "RCDriveModeSet"      # Done
    CMD_RC_SET_FNUMBER          = "RCFNSet"             # Done
    CMD_RC_SET_SHUTTER_SPEED    = "RCShutterSpeedSet"   # Done
    CMD_RC_SET_EV               = "RCEVSet"             # Done
    CMD_RC_SET_ISO              = "RCISOSet"            # Done
    CMD_RC_SET_WB               = "RCWBSet"             # Done
    CMD_RC_SET_COLOR_MODE       = "RCChooseColorMode"   # Done
    CMD_RC_ADJUST_MF            = "RCMFAdjust"
    CMD_RC_DELAY_SHOOT_COUNT    = "RCDShootCntSet"

    CMD_RC_FOCUS                = "RCDoFocus"
    CMD_RC_SHOOT                = "RCDoShooting"        # Done
    