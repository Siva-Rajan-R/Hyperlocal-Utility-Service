from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict, ErrorResponseTypDict, BaseResponseTypDict
from schemas.v1.request_schemas.shop_unit_schema import CreateShopUnitSchema, UpdateShopUnitSchema, DeleteShopUnitSchema, GetShopUnitSchema
from infras.primary_db.services.shop_units_service import ShopUnitService
from fastapi.exceptions import HTTPException

class ShopUnitHandler:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.service = ShopUnitService(session=session)

    async def create(self, data: CreateShopUnitSchema):
        res = await self.service.create(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop unit created successfully",
                    status_code=200,
                    success=True
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Shop Unit",
                description="Invalid data for creating shop unit",
                success=False,
                status_code=400
            )
        )
    

    async def init_units(self, shop_id: str):
        res = await self.service.init_units(shop_id=shop_id)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop unit created successfully",
                    status_code=200,
                    success=True
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Shop Unit",
                description="Invalid data for creating shop unit",
                success=False,
                status_code=400
            )
        )

    async def update(self, data: UpdateShopUnitSchema):
        res = await self.service.update(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop unit updated successfully",
                    status_code=200,
                    success=True
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Updating Shop Unit",
                description="Failed to update or unit is marked as default",
                success=False,
                status_code=400
            )
        )

    async def delete(self, data: DeleteShopUnitSchema):
        try:
            res = await self.service.delete(data=data)
            if res:
                return SuccessResponseTypDict(
                    detail=BaseResponseTypDict(
                        msg="Shop unit deleted successfully",
                        status_code=200,
                        success=True
                    )
                )
            raise Exception("Failed to delete or unit is marked as default")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error - Deleting Shop Unit",
                    description=str(e),
                    success=False,
                    status_code=400
                )
            )

    async def get(self, data: GetShopUnitSchema):
        res = await self.service.get(data=data)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Shop units fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )

    async def getby_id(self, id: str, shop_id: str):
        res = await self.service.getby_id(id=id, shop_id=shop_id)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop unit fetched successfully",
                    status_code=200,
                    success=True
                ),
                data=res
            )
        raise HTTPException(
            status_code=404,
            detail=ErrorResponseTypDict(
                msg="Error - Fetching Shop Unit",
                description="Shop unit not found",
                success=False,
                status_code=404
            )
        )
