import os

import uvicorn
from app.application import app

if __name__ == '__main__':
    uvicorn.run("run:app", log_level="info", reload=True)