import logging


_root_handler = None


def configure_logging(level=logging.DEBUG):
    global _root_handler
    if _root_handler is not None and _root_handler in logging.root.handlers:
        logging.root.removeHandler(_root_handler)
    logging.root.setLevel(logging.NOTSET)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    _root_handler = logging.StreamHandler()
    _root_handler.setFormatter(formatter)
    _root_handler.setLevel(level)
    logging.root.addHandler(_root_handler)
