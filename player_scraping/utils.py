import logging

logger = logging.getLogger(__name__)


def findIndex(labels, label):
    index = 0
    try:
        index = labels.index(label)
        logger.warning(f"{label}: {index}")
        return index
    except ValueError as e:
        return index
