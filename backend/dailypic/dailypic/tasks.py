from celery import shared_task

@shared_task
def last_task():
    print('LAST TASK RUN')

@shared_task
def test_task():
    print('TEST TASK RUN')

@shared_task(bind=True)
def break_chain(self):
    if self.request.chain:
        self.request.chain = self.request.chain[:1]
    return
