from frasco.ext import *
from frasco.utils import import_string
from frasco.models import delayed_tx_calls
from flask_rq2 import RQ
from rq import get_current_job
from .job import FrascoJob
import redis.exceptions
import functools
import logging


logger = logging.getLogger('frasco.tasks')


class FrascoTasksState(ExtensionState):
    def schedule_task(self, pattern, import_name_or_func):
        if isinstance(import_name_or_func, str):
            func = import_string(import_name_or_func)
            import_name = import_name_or_func
        else:
            func = import_name_or_func
            import_name = "%s.%s" % (func.__module__, func.__name__)
        try:
            logger.info("Scheduling task %s at %s" % (import_name, pattern))
            return self.rq.get_scheduler().cron(pattern, func, id="cron-%s" % import_name.replace('.', '-'))
        except redis.exceptions.ConnectionError:
            logger.error("Cannot initialize scheduled tasks as no redis connection is available")


class FrascoTasks(Extension):
    name = 'frasco_tasks'
    state_class = FrascoTasksState
    prefix_extra_options = 'RQ_'

    def _init_app(self, app, state):
        if not app.config.get('RQ_REDIS_URL') and has_extension('frasco_redis', app):
            app.config['RQ_REDIS_URL'] = app.extensions.frasco_redis.options['url']

        app.config.setdefault('RQ_JOB_CLASS', 'frasco.tasks.job.FrascoJob')
        if app.testing:
            app.config.setdefault('RQ_ASYNC', False)
        state.rq = RQ(app)

        for import_name, pattern in state.options.get('schedule', {}).items():
            state.schedule_task(pattern, import_name)


def enqueue_task_now(func, *args, **kwargs):
    return enqueue_now(func, args=args, kwargs=kwargs)


def enqueue_now(func, **options):
    queue_name = options.pop('queue', None)
    return get_extension_state('frasco_tasks').rq.get_queue(queue_name).enqueue_call(func, **options)


def enqueue_task(func, *args, **kwargs):
    return enqueue(func, args=args, kwargs=kwargs)


@delayed_tx_calls.proxy
def enqueue(func, **options):
    return enqueue_now(func, **options)


def get_enqueued_job(id):
    state = get_extension_state('frasco_tasks')
    return FrascoJob.fetch(id, connection=state.rq.connection)


def task(**options):
    def wrapper(func):
        setattr(func, 'enqueue', lambda *a, **kw: enqueue(func, args=a, kwargs=kw, **options))
        setattr(func, 'enqueue_now', lambda *a, **kw: enqueue_now(func, args=a, kwargs=kw, **options))
        return func
    return wrapper
