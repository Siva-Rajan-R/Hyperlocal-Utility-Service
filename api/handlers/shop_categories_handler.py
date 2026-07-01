from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict, ErrorResponseTypDict, BaseResponseTypDict
from schemas.v1.request_schemas.shop_category_schema import CreateShopCategorySchema, UpdateShopCategorySchema, DeleteShopCategorySchema, GetShopCategorySchema
from infras.primary_db.services.shop_categories_service import ShopCategoryService
from fastapi.exceptions import HTTPException

class ShopCategoryHandler:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.service = ShopCategoryService(session=session)

    async def create(self, data: CreateShopCategorySchema):
        res = await self.service.create(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop category created successfully",
                    status_code=200,
                    success=True
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Shop Category",
                description="Invalid data for creating shop category",
                success=False,
                status_code=400
            )
        )
    

    async def init_categories(self, shop_id: str):
        res = await self.service.init_categories(shop_id=shop_id)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop category created successfully",
                    status_code=200,
                    success=True
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Shop Category",
                description="Invalid data for creating shop category",
                success=False,
                status_code=400
            )
        )

    async def update(self, data: UpdateShopCategorySchema):
        res = await self.service.update(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop category updated successfully",
                    status_code=200,
                    success=True
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Updating Shop Category",
                description="Failed to update or category is marked as default",
                success=False,
                status_code=400
            )
        )

    async def delete(self, data: DeleteShopCategorySchema):
        try:
            res = await self.service.delete(data=data)
            if res:
                return SuccessResponseTypDict(
                    detail=BaseResponseTypDict(
                        msg="Shop category deleted successfully",
                        status_code=200,
                        success=True
                    )
                )
            raise Exception("Failed to delete or category is marked as default")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error - Deleting Shop Category",
                    description=str(e),
                    success=False,
                    status_code=400
                )
            )

    async def get(self, data: GetShopCategorySchema):
        res = await self.service.get(data=data)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Shop categories fetched successfully",
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
                    msg="Shop category fetched successfully",
                    status_code=200,
                    success=True
                ),
                data=res
            )
        raise HTTPException(
            status_code=404,
            detail=ErrorResponseTypDict(
                msg="Error - Fetching Shop Category",
                description="Shop category not found",
                success=False,
                status_code=404
            )
        )
