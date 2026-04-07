from enum import Enum

class ServiceTypeEnum(str,Enum):
    PRODUCT="PRODUCT"
    PURCHASE="PURCHASE"
    SHOP="SHOP"
    INVENTORY="INVENTORY"
    EMPLOYEE="EMPLOYEE"
    SUPPLIER="SUPPLIER"