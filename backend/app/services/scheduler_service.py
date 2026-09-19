import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict
from app.database.session import AsyncSessionLocal
from app.repositories.monitor_repo import MonitorRepository
from app.repositories.health_check_repo import HealthCheckRepository
from app.services.checker_service import CheckerService

logger = logging.getLogger("app.scheduler")

# Track last check time per monitor: monitor_id -> timestamp
_last_check_times: Dict[str, float] = {}
_scheduler_task: asyncio.Task | None = None


async def run_scheduler_loop():
    logger.info("Background health check scheduler started.")
    while True:
        try:
            async with AsyncSessionLocal() as db:
                monitor_repo = MonitorRepository(db)
                active_monitors = await monitor_repo.list_all_active()

                now = asyncio.get_event_loop().time()
                for monitor in active_monitors:
                    last_time = _last_check_times.get(monitor.id, 0)
                    if (now - last_time) >= monitor.interval:
                        _last_check_times[monitor.id] = now
                        checker = CheckerService(db)
                        try:
                            check = await checker.perform_check(monitor)
                            logger.info(
                                f"Auto check completed for '{monitor.name}' ({monitor.url}): {check.status} in {check.response_time}ms"
                            )
                        except Exception as e:
                            logger.error(f"Error checking monitor '{monitor.name}': {e}")
        except Exception as e:
            logger.error(f"Error in scheduler loop iteration: {e}")

        # Sleep for a small interval before checking next scheduled batch
        await asyncio.sleep(5)


def start_scheduler():
    global _scheduler_task
    if _scheduler_task is None or _scheduler_task.done():
        _scheduler_task = asyncio.create_task(run_scheduler_loop())


def stop_scheduler():
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
