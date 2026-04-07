from ..models.custom_fields import CustomFields
from sqlalchemy import select,update,delete,case,func,true
from sqlalchemy.ext.asyncio import AsyncSession
from models.repo_models.base_repo_model import BaseRepoModel
from ..models.custom_dropdown import CustomDropdown
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.db_schemas.fields_schema import CreateCustomFieldDbSchema,UpdateCustomFieldSDbSchema
from ..repos.basefields_repo import BaseFieldsRepo
from sqlalchemy.dialects.postgresql import JSONB
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from icecream import ic
from typing import Optional,List
from core.data_formats.typed_dicts.field_typdict import FieldModel
from sqlalchemy.orm import aliased

# 🔥 explode JSON fields
cf = func.jsonb_each(CustomFields.fields)\
    .table_valued("key", "value")\
    .alias("cf")

# extract conn_id
cf_conn_id = cf.c.value.op("->>")("conn_id")

# 🔥 self join alias (for LIST-DICT)
CF_ALIAS = aliased(CustomFields)


# 🚀 MAIN QUERY
query = (
    select(
        CustomFields.id,
        CustomFields.shop_id,
        CustomFields.service_name,
        func.coalesce(
            func.jsonb_object_agg(
                cf.c.key,
                case(

                    # ✅ DROP-DOWN
                    (
                        (cf.c.value.op("->>")("type") == "DROP-DOWN") &
                        (cf_conn_id != None) & (cf_conn_id != ""),
                        cf.c.value.op("||")(
                            func.jsonb_build_object(
                                "values",
                                func.coalesce(
                                    CustomDropdown.values,
                                    func.cast([], JSONB)
                                )
                            )
                        )
                    ),

                    # ✅ LIST-DICT
                    (
                        (cf.c.value.op("->>")("type") == "LIST-DICT") &
                        (cf_conn_id != None) & (cf_conn_id != ""),
                        cf.c.value.op("||")(
                            func.jsonb_build_object(
                                "values",
                                func.coalesce(
                                    CF_ALIAS.fields,
                                    func.cast({}, JSONB)
                                )
                            )
                        )
                    ),

                    # default
                    else_=cf.c.value
                )
            ).filter(cf.c.key != None),
            func.cast({}, JSONB)
        ).label("fields")
    )
    .select_from(CustomFields)

    # explode JSON
    .outerjoin(cf, true())

    # ✅ dropdown join (shop safe)
    .outerjoin(
        CustomDropdown,
        (cf_conn_id == CustomDropdown.id) &
        (CustomDropdown.shop_id == CustomFields.shop_id)
    )

    # 🔥 self join (shop safe)
    .outerjoin(
        CF_ALIAS,
        (cf_conn_id == CF_ALIAS.id) &
        (CF_ALIAS.shop_id == CustomFields.shop_id)
    )

    .group_by(CustomFields.id)
)


class CustomFieldsRepo(BaseRepoModel):
    def __init__(self, session:AsyncSession):
        self.session=session


    @start_db_transaction
    async def create(self,data:CreateCustomFieldDbSchema):
        self.session.add(CustomFields(**data.model_dump(mode='json')))
        
        return True
    
    @start_db_transaction
    async def update(self,id:str,shop_id:str,fields:List[FieldModel]):
        ic("iam in update")
        field_toupdate=update(
            CustomFields
        ).where(
            CustomFields.id==id,
            CustomFields.shop_id==shop_id
        ).values(
            fields=fields
        ).returning(CustomFields.id)

        is_updated=(await self.session.execute(field_toupdate)).scalar_one_or_none()

        return is_updated
    

    @start_db_transaction
    async def update_field(self,data:UpdateCustomFieldSDbSchema):
        is_field_exists=await self.getby_id(field_id=data.id,shop_id=data.shop_id)
        if not is_field_exists:
            return False
        fields=is_field_exists['fields']
        if data.field_name not in fields:
            return False
        
        fields[data.field_name]['label_name']=data.label_name
        fields[data.field_name]['required']=data.required

        field_toupdate=update(
            CustomFields
        ).where(
            CustomFields.id==data.id,
            CustomFields.shop_id==data.shop_id
        ).values(
            fields=fields
        ).returning(CustomFields.id)

        is_updated=(await self.session.execute(field_toupdate)).scalar_one_or_none()

        return is_updated
    
        
    @start_db_transaction
    async def delete(self,field_id:str,shop_id:str,field_name:str):
        fields=(await self.getby_id(field_id=field_id,shop_id=shop_id))
        if not fields or len(fields)<1:
            return False
        
        if field_name not in fields['fields']:
            return False
        
        del fields['fields'][field_name]

        ic(fields['fields'])

        is_updated=await self.update(id=field_id,shop_id=shop_id,fields=fields['fields'])

        return is_updated

    async def get(self):
        field_toget_stmt=select(
            CustomFields.id,
            CustomFields.shop_id,
            CustomFields.fields,
            CustomFields.service_name
        )

        fields=(await self.session.execute(query)).mappings().all()

        return fields
    
    
    async def getby_service_name(self,service_name:str,shop_id:str):
        field_toget_stmt=select(
            CustomFields.id,
            CustomFields.shop_id,
            CustomFields.fields,
            CustomFields.service_name
        ).where(
            CustomFields.service_name==service_name,
            CustomFields.shop_id==shop_id
        )

        field=(await self.session.execute(field_toget_stmt)).mappings().one_or_none()

        return field
    
    async def getby_id(self,field_id:str,shop_id:str):
        field_toget_stmt=select(
            CustomFields.id,
            CustomFields.shop_id,
            CustomFields.fields,
            CustomFields.service_name
        ).where(
            CustomFields.id==field_id,
            CustomFields.shop_id==shop_id
        )

        field=(await self.session.execute(field_toget_stmt)).mappings().one_or_none()

        return field
    

    async def search(self, query, limit = 5):
        ...


        

    