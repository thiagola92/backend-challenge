from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.routers import alerts, camera, cameras
from src.security import login
from src.setup import lifespan

app = FastAPI(lifespan=lifespan)


app.include_router(alerts.router)
app.include_router(camera.router)
app.include_router(cameras.router)
app.include_router(login.router)


@app.get("/", include_in_schema=False)
async def root():
    return HTMLResponse(
        content="""
        <html>
            <body>
                Documentation at: <a href="/docs/">/docs/</a> <br/>
                Access Token at: <a href="/token/">/token/</a> <br/>
            </body>
        </html>
        """
    )
