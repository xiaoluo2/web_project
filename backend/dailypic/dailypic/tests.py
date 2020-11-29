from django.test import TestCase
from .tasks import test_task, break_chain, last_task
from celery import chain

class CeleryTestCase():
    # should only print 'LAST TASK RUN'
    def test_chain_break(self):
        chain = (break_chain.si()|test_task.si()|test_task.si()|test_task.si()|test_task.si()|test_task.si()|test_task.si()|last_task.si())
        chain()
