from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pydantic import BaseModel
from collections.abc import Iterator
from typing import Callable, Union, Any, Optional, List

# this will come from monologue when mature
from apin.core.ops.inspector import inspect_modules
import apin

from functools import partial
from loguru import logger
import warnings

EVENT_TYPE = Union[BaseModel, List[BaseModel], dict, List[dict]]

# im ignoring the apscheduler induced time zone warning (and everything else for now)
warnings.filterwarnings("ignore")


class ScheduledTask(BaseModel):
    name: str
    namespace: str
    runner: Callable
    hour: Union[Any, None] = None
    minute: Union[Any, None] = None
    day: Union[Any, None] = None


def invoke_task(
    name: str, event: Optional[EVENT_TYPE] = None, options: Optional[dict] = None
):
    logger.info("Invoked")


def _get_scheduled_jobs() -> Iterator[ScheduledTask]:
    """
    We have an understanding with the modules
    - they decide for themselves via attributes if they want to be invoked on a schedule
    """
    logger.info(f"Fetching tasks to schedule from APIN")
    for op in inspect_modules(apin):
        if op.interval_minutes or op.interval_days or op.interval_hours:
            yield ScheduledTask(
                name=op.name,
                namespace=op.namespace,
                # we just partially eval this just so the scheduler has something it can easily run
                # this will call an api e.g. rest with the right params
                runner=partial(invoke_task, name=op.namespace),
                # we specify how often we want to kick of this task
                minute=op.interval_minutes,
            )


def start_scheduler():
    """
    Start the scheduler. Load all the callable functions that have attributes for scheduling
    """
    scheduler = BlockingScheduler({"apscheduler.timezone": "UTC"})
    for task in _get_scheduled_jobs():
        logger.info(f"<< Adding to schedule task {task} >>")
        scheduler.add_job(
            task.runner,
            CronTrigger(
                start_date="2023-1-1", hour=task.hour, minute=task.minute, day=task.day
            ),
            id=task.name,
            replace_existing=True,
            args=None,
        )
    scheduler.start()
    return scheduler
