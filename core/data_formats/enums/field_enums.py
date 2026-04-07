from enum import Enum


class FieldTypeEnum(str,Enum):
    DROP_DOWN="DROP-DOWN"
    TEXT="TEXT"
    NUMBER="NUMBER"
    DECIMAL="DECIMAL"
    TEXTAREA="TEXTAREA"
    EMAIL="EMAIL"
    DATE="DATE"
    BOOLEAN="BOOLEAN"
    LIST_DICT="LIST-DICT"
    DICT="DICT"

class ViewModeEnum(str,Enum):
    HIDE="HIDE"
    SHOW="SHOW"

