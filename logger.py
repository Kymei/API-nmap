import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="",
    datefmt="%Y-%m-%d %H:%M:%S"
)

lg = logging.getLogger(__name__)
