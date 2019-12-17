from apscheduler.schedulers.blocking import BlockingScheduler

from update_db import update

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=120)
def timed_job():
    update()
    print('DB updated')

sched.start()
