from enum import Enum

class CmdEnumFileQuality(str, Enum):
    Best = "Original"
    Medium = "MidThumb"
    Fast = "Thumbnail"