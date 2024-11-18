from controller.controllers import app
from common.config import DEBUG, HTTP_HOST, HTTP_PORT
from model.db import createDB

def main() -> None:
    createDB()
    app.run(HTTP_HOST, HTTP_PORT, DEBUG)


if __name__ == "__main__":
    main()
