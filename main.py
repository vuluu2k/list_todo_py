import uvicorn
from decouple import config

if __name__ == '__main__':
    print(config("SECRET"))
    uvicorn.run('app.api:app', port=8000, host="localhost", reload=True)
