from fastapi import FastAPI
from app.dataroutes import router as data_router
from app.docroutes import router as docs_router
from app.pages.pagesrouter import router as pages_router
from app.templates.graphs.graphroutes import router as graph_router
from fastapi.staticfiles import StaticFiles



app = FastAPI(
    title="Rul Project"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(docs_router)
app.include_router(data_router)
app.include_router(pages_router)
app.include_router(graph_router)

@app.get("/")
async def root():
    return {"message": "Welcome rul prognostics api!"}

