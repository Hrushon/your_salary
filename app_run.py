import uvicorn

from src.api_main import create_application

app = create_application()

if __name__ == '__main__':
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
