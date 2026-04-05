import logging

# Razorpay API base URLs
RAZORPAY_API_V1 = "https://api.razorpay.com/v1"
RAZORPAY_API_V2 = "https://api.razorpay.com/v2"

# Default pagination size
DEFAULT_COUNT = 10
MAX_COUNT = 100


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
