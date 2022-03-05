from datetime import datetime, time
from django.core.mail import send_mail
from arikeapp.models import *
from datetime import datetime, timedelta, timezone
from arikeproject.celery import app
from django.db import transaction

@app.task
def send_email_report(report):
    currentTime = datetime.now()
    start = currentTime(timezone.utc) - timedelta(days=1)
    nurses=Myuser.objects.filter(deleted=False, role='Primary Nurse') | Myuser.objects.filter(deleted=False, role='Secondary Nurse')
    
    for nurse in nurses:
        patients_count= Visit_schedule.objects.filter(deleted=False, nurse=nurse, updated_at__lt=start ).count()
        email_content = f"""
        Hi {nurse.first_name} {nurse.last_name},
        \n\nYour daily report: \n
        No. of patients handled =   {patients_count} \n
        Treatments done = {2} \n
       
        \n\nRegards,\nYour Wonderful Arike App
    """
        send_mail("Daily Patients Report", email_content, "arikeapp@gdc.com", nurse.email )
    
    


@app.task
def periodic_emailer():
    currentTime = datetime.now()
    start = currentTime(timezone.utc) - timedelta(days=1)
    with transaction.atomic():
        reports = Nurses_Report.objects.select_for_update().filter(
            last_updated__lt=start,
            confirmation=True
        )
        for r in reports:
            send_email_report(r)
            r.last_updated = datetime.now(timezone.utc).replace(hour=r.time.hour, minute=r.time.minute,
                second=r.time.second)
            r.save()


app.conf.beat_schedule={"send-patients-report" : {
    'task': 'arikeapp.tasks.periodic_emailer',
    'schedule': 60.0,
},
}
