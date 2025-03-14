import uvicorn

from config import (OPENAI_API_KEY)
from driver import create_driver
from api import create_api


api_key = OPENAI_API_KEY
driver = create_driver
app = create_api

@app.on_event("shutdown")
def shutdown_event():
    driver.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)