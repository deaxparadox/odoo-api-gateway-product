from celery import shared_task
from celery.utils.log import get_task_logger
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.utils import aware_utcnow

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")
    
@shared_task
def removed_expired_tokens():
    print("Removing expired Outstanding tokens")
    OutstandingToken.objects.filter(expires_at__lte=aware_utcnow())