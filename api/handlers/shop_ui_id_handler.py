from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from hyperlocal_platform.core.models.req_res_models import (
    SuccessResponseTypDict,
    ErrorResponseTypDict,
    BaseResponseTypDict,
)

from schemas.v1.request_schemas.shop_ui_id_schema import (
    CreateShopUiIdSchema,
    UpdateShopUiIdSchema,
    DeleteShopUiIdSchema,
    GetShopUiIdSchema,
)

from infras.primary_db.services.shop_ui_id_service import ShopUiIdService


class ShopUiIdHandler:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.service = ShopUiIdService(session=session)

    async def init_ids(self,shop_id):
        res = await self.service.init_ids(shop_id=shop_id)

        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop UI ID created successfully",
                    status_code=200,
                    success=True,
                )
            )

        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Shop UI ID",
                description="Invalid data for creating Shop UI ID",
                success=False,
                status_code=400,
            ),
        )

    async def create(self, data: CreateShopUiIdSchema):
        res = await self.service.create(data=data)

        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop UI ID created successfully",
                    status_code=200,
                    success=True,
                )
            )

        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Shop UI ID",
                description="Invalid data for creating Shop UI ID",
                success=False,
                status_code=400,
            ),
        )

    async def update(self, data: UpdateShopUiIdSchema):
        res = await self.service.update(data=data)

        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop UI ID updated successfully",
                    status_code=200,
                    success=True,
                )
            )

        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Updating Shop UI ID",
                description="Failed to update Shop UI ID",
                success=False,
                status_code=400,
            ),
        )

    async def delete(self, data: DeleteShopUiIdSchema):
        try:
            res = await self.service.delete(data=data)

            if res:
                return SuccessResponseTypDict(
                    detail=BaseResponseTypDict(
                        msg="Shop UI ID deleted successfully",
                        status_code=200,
                        success=True,
                    )
                )

            raise Exception("Failed to delete Shop UI ID")

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error - Deleting Shop UI ID",
                    description=str(e),
                    success=False,
                    status_code=400,
                ),
            )

    async def get(self, data: GetShopUiIdSchema):
        res = await self.service.get(data=data)

        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Shop UI IDs fetched successfully",
                status_code=200,
                success=True,
            ),
            data=res,
        )

    async def getby_id(self, id: str, shop_id: str):
        res = await self.service.getby_id(
            id=id,
            shop_id=shop_id,
        )

        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop UI ID fetched successfully",
                    status_code=200,
                    success=True,
                ),
                data=res,
            )

        raise HTTPException(
            status_code=404,
            detail=ErrorResponseTypDict(
                msg="Error - Fetching Shop UI ID",
                description="Shop UI ID not found",
                success=False,
                status_code=404,
            ),
        )

    async def get_by_entity_type(
        self,
        shop_id: str,
        entity_type: str,
    ):
        res = await self.service.get_by_entity_type(
            shop_id=shop_id,
            entity_type=entity_type,
        )

        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop UI ID fetched successfully",
                    status_code=200,
                    success=True,
                ),
                data=res,
            )

        raise HTTPException(
            status_code=404,
            detail=ErrorResponseTypDict(
                msg="Error - Fetching Shop UI ID",
                description="Configuration not found for the specified entity type",
                success=False,
                status_code=404,
            ),
        )

    async def get_next_number(
        self,
        shop_id: str,
        entity_type: str,
    ):
        res = await self.service.get_next_number(
            shop_id=shop_id,
            entity_type=entity_type,
        )

        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Current number incremented successfully",
                    status_code=200,
                    success=True,
                ),
                data=res,
            )

        raise HTTPException(
            status_code=404,
            detail=ErrorResponseTypDict(
                msg="Error - Incrementing Current Number",
                description="Shop UI ID configuration not found",
                success=False,
                status_code=404,
            ),
        )
