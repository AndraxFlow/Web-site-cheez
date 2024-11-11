from backend.controllers import app
from backend.config import DEBUG, HTTP_HOST, HTTP_PORT
from backend.db import createDB

def main() -> None:
    createDB()
    app.run(HTTP_HOST, HTTP_PORT, DEBUG)
    
    
if __name__ == "__main__":
    main()