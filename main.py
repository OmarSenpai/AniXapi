import uvicorn
import config
from config import app

if __name__ == "main":
    print(f"Starting{config.PROJECT_NAME} v{config.VERSION}"
          f"in {'DEBUG' if config.DEBUG_MODE else 'PRODUCTION'} mode ...")
    uvicorn.run("127.0.0.1", 8000)
