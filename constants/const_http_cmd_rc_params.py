from enum import StrEnum

class RcMeteringMode(StrEnum):
    Multi = "Multi"
    Spot = "Spot"
    CenterWeighted = "CenterWeighted"

class RcExposureMode(StrEnum):
    Auto = "Auto"
    Program = "P"
    AperturePriority = "A"
    ShutterPriority = "S"
    Manual = "M"
    MasterGuide = "C"

class RcFocusMode(StrEnum):
    ContrastAutofocus = "C-AF"
    SingleAreaAutofocus = "S-AF"
    ManualFocus = "MF"

class RcImageQuality(StrEnum):
    MP50_Interpolated = "50"
    MP20 = "20"
    MP16 = "16"
    MP8 = "8"
    MP3 = "3"
    VGA = "VGA"

class RcImageAspect(StrEnum):
    A43 = "4:3"
    A32 = "3:2"
    Widescreen = "16:9"
    Square = "1:1"

class RcFileFormat(StrEnum):
    Raw = "RAW"
    JpegSmall = "JPG-S"
    JpegMedium = "JPG-M"
    JpegLarge = "JPG-L"
    RawAndJpegSmall = "RAWJ-S"
    RawAndJpegMedium = "RAWJ-M"
    RawAndJpegLarge = "RAWJ-L"

class RcDriveMode(StrEnum):
    Single = "Single"
    Continuous = "Continuous"
    Delay2 = "2SDelay"
    Delay10 = "10SDelay"

class RcFStop(StrEnum):
    F1p0 = "1.0"
    F1p2 = "1.2"
    F1p4 = "1.4"
    F1p7 = "1.7"
    F1p8 = "1.8"
    F2p0 = "2.0"
    F2p2 = "2.2"
    F2p5 = "2.5"
    F2p8 = "2.8"
    F3p2 = "3.2"
    F3p5 = "3.5"
    F4p0 = "4.0"
    F4p5 = "4.5"
    F5p0 = "5.0"
    F5p6 = "5.6"
    F6p3 = "6.3"
    F7p1 = "7.1"
    F8p0 = "8.0"
    F9p0 = "9.0"
    F10 = "10"
    F11 = "11"
    F13 = "13"
    F14 = "14"
    F16 = "16"
    F18 = "18"
    F20 = "20"
    F22 = "22"
    F25 = "25"
    F29 = "29"
    F32 = "32"

class RcIso(StrEnum):
    Auto = "Auto"
    I100 = "100"
    I200 = "200"
    I400 = "400"
    I800 = "800"
    I1600 = "1600"
    I3200 = "3200"
    I6400 = "6400"
    I12800 = "12800"
    I25600 = "25600"

class RcWhiteBalance(StrEnum):
    Auto = "Auto"
    Sunny = "Sunny"
    Cloudy = "Cloudy"
    Shadow = "Shadow"
    Incandescent = "Incandescent"
    K2000 = "2000"
    K2050 = "2050"
    K2100 = "2100"
    K2150 = "2150"
    K2200 = "2200"
    K2250 = "2250"
    K2300 = "2300"
    K2350 = "2350"
    K2400 = "2400"
    K2450 = "2450"
    K2500 = "2500"
    K2550 = "2550"
    K2600 = "2600"
    K2650 = "2650"
    K2700 = "2700"
    K2750 = "2750"
    K2800 = "2800"
    K2850 = "2850"
    K2900 = "2900"
    K2950 = "2950"
    K3000 = "3000"
    K3100 = "3100"
    K3200 = "3200"
    K3300 = "3300"
    K3400 = "3400"
    K3500 = "3500"
    K3600 = "3600"
    K3700 = "3700"
    K3800 = "3800"
    K3900 = "3900"
    K4000 = "4000"
    K4200 = "4200"
    K4400 = "4400"
    K4600 = "4600"
    K4800 = "4800"
    K5000 = "5000"
    K5200 = "5200"
    K5400 = "5400"
    K5600 = "5600"
    K5800 = "5800"
    K6000 = "6000"
    K6200 = "6200"
    K6400 = "6400"
    K6600 = "6600"
    K6800 = "6800"
    K7000 = "7000"
    K7500 = "7500"
    K8000 = "8000"
    K8500 = "8500"
    K9000 = "9000"
    K9500 = "9500"
    K10000 = "10000"
    K10500 = "10500"
    K11000 = "11000"
    K11500 = "11500"

class RcShutterSpeed(StrEnum):
    Time = "TIME"
    Bulb = "BULB"
    S60 = "60s"
    S50 = "50s"
    S40 = "40s"
    S30 = "30s"
    S25 = "25s"
    S20 = "20s"
    S15 = "15s"
    S13 = "13s"
    S10 = "10s"
    S8 = "8s"
    S6 = "6s"
    S5 = "5s"
    S4 = "4s"
    S3p2 = "3.2s"
    S2p5 = "2.5s"
    S2 = "2s"
    S1p6 = "1.6s"
    S1p3 = "1.3s"
    S1 = "1s"
    SF1p3 = "1/1.3s"
    SF1p6 = "1/1.6s"
    SF2 = "1/2s"
    SF2p5 = "1/2.5s"
    SF3 = "1/3s"
    SF4 = "1/4s"
    SF5 = "1/5s"
    SF6 = "1/6s"
    SF8 = "1/8s"
    SF10 = "1/10s"
    SF13 = "1/13s"
    SF15 = "1/15s"
    SF20 = "1/20s"
    SF25 = "1/25s"
    SF30 = "1/30s"
    SF40 = "1/40s"
    SF50 = "1/50s"
    SF60 = "1/60s"
    SF80 = "1/80s"
    SF100 = "1/100s"
    SF125 = "1/125s"
    SF160 = "1/160s"
    SF200 = "1/200s"
    SF250 = "1/250s"
    SF320 = "1/320s"
    SF400 = "1/400s"
    SF500 = "1/500s"
    SF640 = "1/640s"
    SF800 = "1/800s"
    SF1000 = "1/1000s"
    SF1250 = "1/1250s"
    SF1600 = "1/1600s"
    SF2000 = "1/2000s"
    SF2500 = "1/2500s"
    SF3200 = "1/3200s"
    SF4000 = "1/4000s"

class RcColorStyle(StrEnum):
    Standard = "Standard"
    Portrait = "Portrait"
    Vivid = "Vivid"
    NaturalBW = "NaturalBW"
    HighContrastBW = "HContrastBW"

class RcEvOffset(StrEnum):
    N5p0 = "-5.0"
    N4p7 = "-4.7"
    N4p3 = "-4.3"
    N4p0 = "-4.0"
    N3p7 = "-3.7"
    N3p3 = "-3.3"
    N3p0 = "-3.0"
    N2p7 = "-2.7"
    N2p3 = "-2.3"
    N2p0 = "-2.0"
    N1p7 = "-1.7"
    N1p3 = "-1.3"
    N1p0 = "-1.0"
    N0p7 = "-0.7"
    N0p3 = "-0.3"
    Zero = "0.0"
    P0p3 = "0.3"
    P0p7 = "0.7"
    P1p0 = "1.0"
    P1p3 = "1.3"
    P1p7 = "1.7"
    P2p0 = "2.0"
    P2p3 = "2.3"
    P2p7 = "2.7"
    P3p0 = "3.0"
    P3p3 = "3.3"
    P3p7 = "3.7"
    P4p0 = "4.0"
    P4p3 = "4.3"
    P4p7 = "4.7"
    P5p0 = "5.0"