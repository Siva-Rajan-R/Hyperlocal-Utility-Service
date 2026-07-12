from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List

class SubUnitSchema(BaseModel):
    name: str
    factor: float

    @field_validator('factor')
    @classmethod
    def validate_factor(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Conversion factor must be greater than zero")
        return v

class CreateShopUnitSchema(BaseModel):
    shop_id: str
    name: str
    short_name: str
    description: Optional[str] = None
    is_active: bool = True
    sub_units: Optional[List[SubUnitSchema]] = None

    @model_validator(mode='after')
    def validate_sub_units(self) -> 'CreateShopUnitSchema':
        if not self.sub_units:
            return self
        
        base_name_lower = self.name.lower()
        seen_names = set()
        seen_factors = set()
        
        for su in self.sub_units:
            su_name_lower = su.name.lower()
            if su_name_lower == base_name_lower:
                raise ValueError(f"Base unit '{self.name}' cannot be added as a sub unit")
            if su_name_lower in seen_names:
                raise ValueError(f"Duplicate sub unit name: {su.name}")
            if su.factor in seen_factors:
                raise ValueError(f"Duplicate conversion factor: {su.factor}")
            seen_names.add(su_name_lower)
            seen_factors.add(su.factor)
            
        return self

class UpdateShopUnitSchema(BaseModel):
    id: str
    shop_id: str
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sub_units: Optional[List[SubUnitSchema]] = None

    @model_validator(mode='after')
    def validate_sub_units(self) -> 'UpdateShopUnitSchema':
        if not self.sub_units:
            return self
        
        seen_names = set()
        seen_factors = set()
        base_name_lower = self.name.lower() if self.name else None
        
        for su in self.sub_units:
            su_name_lower = su.name.lower()
            if base_name_lower and su_name_lower == base_name_lower:
                raise ValueError(f"Base unit '{self.name}' cannot be added as a sub unit")
            if su_name_lower in seen_names:
                raise ValueError(f"Duplicate sub unit name: {su.name}")
            if su.factor in seen_factors:
                raise ValueError(f"Duplicate conversion factor: {su.factor}")
            seen_names.add(su_name_lower)
            seen_factors.add(su.factor)
            
        return self

class DeleteShopUnitSchema(BaseModel):
    id: str
    shop_id: str

class GetShopUnitSchema(BaseModel):
    shop_id: str
    limit: int = Field(default=10, le=100)
    offset: int = Field(default=1)
    is_active: Optional[bool] = None
