import settings
from app.services import StdInLogClient

if __name__ == "__main__":
    stdin_log_producer = StdInLogClient(settings.LOG_SERVER_HOST, settings.LOG_SERVER_PORT)
    stdin_log_producer.start()
