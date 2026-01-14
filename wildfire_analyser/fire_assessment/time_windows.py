# date_utils.py
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def compute_fire_time_windows(
    start_date: str,
    end_date: str,
    buffer_days: int,
) -> tuple[str, str, str, str]:
    sd = datetime.strptime(start_date, "%Y-%m-%d")
    ed = datetime.strptime(end_date, "%Y-%m-%d")
    before_start = (sd - timedelta(days=buffer_days)).strftime("%Y-%m-%d")
    after_end = (ed + timedelta(days=buffer_days)).strftime("%Y-%m-%d")
    return before_start, start_date, end_date, after_end

