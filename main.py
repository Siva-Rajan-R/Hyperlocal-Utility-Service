from fastapi import FastAPI
from api.routers.v1 import customdropdown_routes,customfields_routes,basedropdown_routes,basefields_routes,shop_ui_id_routes
from infras.primary_db.services.shop_units_service import ShopUnitService
from infras.primary_db.services.shop_categories_service import ShopCategoryService
from infras.primary_db.services.shop_ui_id_service import ShopUiIdService
from contextlib import asynccontextmanager
from icecream import ic
from dotenv import load_dotenv
from infras.primary_db.main import init_utilis_pg_db
from core.configs.settings_config import SETTINGS
from hyperlocal_platform.core.enums.environment_enum import EnvironmentEnum
import os,asyncio
from hyperlocal_platform.infras.saga.main import init_infra_db
from infras.primary_db.main import AsyncUtilisLocalSession
from fastapi.middleware.cors import CORSMiddleware
from messaging.worker import worker
load_dotenv()


@asynccontextmanager
async def utility_service_lifespan(app:FastAPI):
    try:
        ic("Starting utility service...")
        await init_utilis_pg_db()
        # await redis_client.flushdb()
        # async with AsyncUtilisLocalSession() as session:
        #     await ShopUiIdService(session=session).init_ids(shop_id="string")
        #     await ShopUnitService(session=session).init_units(shop_id="string")
        #     await ShopCategoryService(session=session).init_categories(shop_id="string")
        asyncio.create_task(worker())
        yield

    except Exception as e:
        ic(f"Error : Starting utility service => {e}")

    finally:
        ic("...Stoping utility Servcie...")

debug=False
openapi_url=None
docs_url=None
redoc_url=None

if SETTINGS.ENVIRONMENT.value==EnvironmentEnum.DEVELOPMENT.value:
    debug=True
    openapi_url="/openapi.json"
    docs_url="/docs"
    redoc_url="/redoc"

app=FastAPI(
    title="Utility Service",
    description="This service contains all the CRUD operations for Utility service",
    debug=debug,
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    lifespan=utility_service_lifespan,
    root_path="/utilities"
    
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# Routes to include
# app.include_router(basefields_routes.router)
# app.include_router(customfields_routes.router)
# app.include_router(basedropdown_routes.router)
# app.include_router(customdropdown_routes.router)


from api.routers.v1 import activity_log_routes, upload_routes, shopidconfig_routes, shop_categories_routes, shop_units_routes
app.include_router(activity_log_routes.router)
app.include_router(upload_routes.router)
app.include_router(shopidconfig_routes.router)
app.include_router(shop_categories_routes.router)
app.include_router(shop_units_routes.router)
app.include_router(shop_ui_id_routes.router)



