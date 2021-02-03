from src.models import Alert
from src.common import logger

# Setup cronjob
# See https://towardsdatascience.com/scheduling-all-kinds-of-recurring-jobs-with-python-b8784c74d5dc

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()

if not alerts:
    logger.info("No alerts have been created. Create an alert to get started.")


