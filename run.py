import multiprocessing
from app import app

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app.run(port=5000)