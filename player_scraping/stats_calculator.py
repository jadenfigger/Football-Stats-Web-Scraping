import logging
from .utils import get_value_at_index

logger = logging.getLogger(__name__)


class StatCalculator:
    """Will calculate the points for any NFL player
       based on a stats list in a specified format
       [pass_yds, rush_atms, rush_yds, tot_rec, rec_yds, touchdowns]
    Returns:
        Float: Points for player
    """

    @staticmethod
    def calculate_points(stats):
        # You can modify this formula based on your league's point system
        # stats = [pass_yds, rush_atms, rush_yds, tot_rec, rec_yds, touchdowns]
        logger.warning(stats)
        points = (
            stats[0] * 0.05
            + stats[1] * 0.1
            + stats[2] * 0.1
            + stats[4] * 0.1
            + stats[5] * 6
            + stats[3]
        )
        if stats[0] >= 300:
            points += 5
        if stats[2] >= 100:
            points += 5
        if stats[4] >= 150:
            points += 5

        logger.warning(points)
        return points

    """
    Will accept the labels and gameStats for a NFL player
    The labels is list that will serve as a reference
    to extract the neccesary stats for each player (due
    to different positions returning different gameStats)
    Returns:
        list: stats for player in the format (pass_yds, rush_atms, rush_yds, tot_rec, rec_yds, touchdowns)
    """

    @staticmethod
    def extract_stats(labels, gameStats):
        stats = []
        stats.append(get_value_at_index(labels, "passingYards", gameStats))
        stats.append(get_value_at_index(labels, "rushingAttempts", gameStats))
        stats.append(get_value_at_index(labels, "rushingYards", gameStats))
        stats.append(get_value_at_index(labels, "receptions", gameStats))
        stats.append(get_value_at_index(labels, "receivingYards", gameStats))
        stats.append(
            get_value_at_index(labels, "rushingTouchdowns", gameStats)
            + get_value_at_index(labels, "passingTouchdowns", gameStats)
            + get_value_at_index(labels, "receivingTouchdowns", gameStats)
        )

        return stats
