import logging
from datetime import datetime

from django.db.utils import IntegrityError

from part.models import Part

logger = logging.getLogger(__name__)


def add_part(reference: str, source: str):
    log_message = lambda message: f"{datetime.now()}: Part:{reference} {message}"

    try:
        Part.objects.create(reference=reference, source=source)
    except IntegrityError:
        logger.info(log_message("already in"))
    except Exception as error:
        logger.info(log_message(error))
    else:
        logger.info(log_message("added"))
