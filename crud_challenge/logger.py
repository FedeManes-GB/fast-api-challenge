import logging

# Basic logging config
logging.basicConfig(
    level=logging.INFO,  # You can change to DEBUG, WARNING, ERROR, etc.
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
