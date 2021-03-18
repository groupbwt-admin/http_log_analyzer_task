import settings
from app.services import HTTPOverloadingPeriodAnalyzer
from app.utils import configure_logging


if __name__ == "__main__":
    configure_logging(settings.LOG_LEVEL)
    overloading_analyzer = HTTPOverloadingPeriodAnalyzer(
        settings.LOG_SERVER_HOST,
        settings.LOG_SERVER_PORT,
        settings.ESTIMATOR
    )
    overloading_analyzer.start()
