from random import choices
from string import ascii_uppercase, digits
import time

from uvicorn import run
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.types import ASGIApp, Scope, Receive, Send

from util.logger import logger


class AuthMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        logger.debug(scope.get('path'))
        await self.app(scope, receive, send)


def create_app():

    app = FastAPI(title='贵师大大数据B站舆情分析', description='消防调度')

    origins = [
        "http://172.22.78.101:3333",
        "http://localhost:3333",
        "http://127.0.0.1:8000/",
        "http://127.0.0.1:8000",

    ]
    app.add_middleware(AuthMiddleware)  # 这个一定要放到CORSMiddleware前面
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    api_version = '/api/v1'
    from api.login.login import router as login
    app.include_router(login, prefix=api_version, tags="登录注册")

    from api.search.t_fire import router as search_fire
    app.include_router(search_fire, prefix=api_version+"/search/fire", tags=['事故信息'])

    from api.search.station import router as station_info
    app.include_router(station_info, prefix=api_version + "/search/station", tags=['消防站信息'])

    return app


app = create_app()



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.url.path.startswith('/static/'):
        return await call_next(request)
    idem = ''.join(choices(ascii_uppercase + digits, k=8))
    start = time.time()
    logger.info(f"rid={idem}     start request {request.method} path={request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem}     end request elapsed={formatted_process_time}ms status_code={response.status_code}")
    return response


# 全局统一异常处理
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except BaseException as e:
        return JSONResponse(status_code=200, content={"status": 400, "msg": f"错误信息：" + str(e), "data": {}})

app.mount("/static", StaticFiles(directory="dist\static"), name="static")
templates = Jinja2Templates(directory="dist")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def start():
    import uvicorn
    uvicorn.run(app='main:app', host='0.0.0.0', port=33333, reload=True, debug=True, log_level='info')


if __name__ == '__main__':
    start()