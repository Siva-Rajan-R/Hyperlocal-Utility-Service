from ..models.base_fields import BaseFields
from sqlalchemy import select,update,delete,case,func,true
from sqlalchemy.orm import aliased
from ..models.base_dropdown import BaseDropdown
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from models.repo_models.base_repo_model import BaseRepoModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.db_schemas.fields_schema import CreateBaseFieldDbSchema,UpdateBaseFieldSDbSchema
from icecream import ic
from typing import Optional,List
from core.data_formats.typed_dicts.field_typdict import FieldModel

# 🔥 JSONB explode
f = func.jsonb_each(BaseFields.fields)\
    .table_valued("key", "value")\
    .alias("f")

# extract conn_id
conn_id = f.c.value.op("->>")("conn_id")

# 🔥 self join alias for LIST-DICT
BF_ALIAS = aliased(BaseFields)


# 🚀 MAIN QUERY
query = (
    select(
        BaseFields.id,
        BaseFields.service_name,
        func.coalesce(
            func.jsonb_object_agg(
                f.c.key,
                case(

                    # ✅ DROP-DOWN
                    (
                        (f.c.value.op("->>")("type") == "DROP-DOWN") &
                        (conn_id != None) & (conn_id != ""),
                        f.c.value.op("||")(
                            func.jsonb_build_object(
                                "values",
                                func.coalesce(
                                    BaseDropdown.values,
                                    func.cast([], JSONB)
                                )
                            )
                        )
                    ),

                    # ✅ LIST-DICT
                    (
                        (f.c.value.op("->>")("type") == "LIST-DICT") &
                        (conn_id != None) & (conn_id != ""),
                        f.c.value.op("||")(
                            func.jsonb_build_object(
                                "values",
                                func.coalesce(
                                    BF_ALIAS.fields,
                                    func.cast({}, JSONB)
                                )
                            )
                        )
                    ),

                    # default
                    else_=f.c.value
                )
            ).filter(f.c.key != None),
            func.cast({}, JSONB)
        ).label("fields")
    )
    .select_from(BaseFields)
    .outerjoin(f, true())

    # dropdown join
    .outerjoin(
        BaseDropdown,
        conn_id == BaseDropdown.id
    )

    # 🔥 self join for LIST-DICT
    .outerjoin(
        BF_ALIAS,
        conn_id == BF_ALIAS.id
    )

    .group_by(BaseFields.id)
)

class BaseFieldsRepo(BaseRepoModel):
    def __init__(self, session:AsyncSession):
        self.session=session


    @start_db_transaction
    async def create(self,data:CreateBaseFieldDbSchema):
        self.session.add(BaseFields(**data.model_dump(mode='json')))
        
        return True
    
    @start_db_transaction
    async def update(self,id:str,fields:List[FieldModel]):
        ic("iam in update")
        field_toupdate=update(
            BaseFields
        ).where(
            BaseFields.id==id
        ).values(
            fields=fields
        ).returning(BaseFields.id)

        is_updated=(await self.session.execute(field_toupdate)).scalar_one_or_none()

        return is_updated
    

    @start_db_transaction
    async def update_field(self,data:UpdateBaseFieldSDbSchema):
        is_field_exists=await self.getby_id(field_id=data.id)
        if not is_field_exists:
            return False
        fields=is_field_exists['fields']
        if data.field_name not in fields:
            return False
        
        fields[data.field_name]['label_name']=data.label_name
        fields[data.field_name]['required']=data.required

        field_toupdate=update(
            BaseFields
        ).where(
            BaseFields.id==data.id,
        ).values(
            fields=fields
        ).returning(BaseFields.id)

        is_updated=(await self.session.execute(field_toupdate)).scalar_one_or_none()

        return is_updated
        
    @start_db_transaction
    async def delete(self,field_id:str,field_name:str):
        fields=(await self.getby_id(field_id=field_id))
        ic(fields)
        if not fields or len(fields)<1:
            return False
        if field_name not in fields['fields']:
            return False
         
        del fields['fields'][field_name]
        is_updated=await self.update(id=field_id,fields=fields['fields'])

        return is_updated

    async def get(self):
        field_toget_stmt=select(
            BaseFields.fields,
            BaseFields.id,
            BaseFields.service_name
        )

        fields=(await self.session.execute(query)).mappings().all()

        return fields
    
    async def getby_service_name(self,service_name:str):
        field_toget_stmt=select(
            BaseFields.fields,
            BaseFields.id,
            BaseFields.service_name
        ).where(
            BaseFields.service_name==service_name
        )

        modified_query=query.where(BaseFields.service_name==service_name)

        field=(await self.session.execute(modified_query)).mappings().one_or_none()

        ic(field)

        return field
    
    async def getby_id(self,field_id:str):
        field_toget_stmt=select(
            BaseFields.fields,
            BaseFields.id,
            BaseFields.service_name
        ).where(
            BaseFields.id==field_id
        )

        modified_query=query.where(BaseFields.id==field_id)

        field=(await self.session.execute(modified_query)).mappings().one_or_none()

        return field
    

    async def search(self, query, limit = 5):
        ...


        

    