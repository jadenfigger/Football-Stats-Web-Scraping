import logging

logger = logging.getLogger(__name__)


def get_value_at_index(labels, label, stats):
    index = find_index(labels, label)
    if not index:
        return 0
    return float(stats[index])


def find_index(labels, label):
    index = None
    try:
        index = list(labels).index(label)
        logger.warning(f"{label}: {index}")
        return index
    except ValueError as e:
        return index
