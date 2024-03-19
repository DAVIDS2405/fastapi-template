import uvicorn
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    uvicorn.run("server:app", host=HOST, port=int(PORT), reload=True)
