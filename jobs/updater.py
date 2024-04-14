from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api, cleanup
import os

def start():
    run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
    if run_once is not None:
        return
    os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api, 'interval', seconds=100)
    scheduler.add_job(cleanup, 'cron', minute=46)
    scheduler.start()
