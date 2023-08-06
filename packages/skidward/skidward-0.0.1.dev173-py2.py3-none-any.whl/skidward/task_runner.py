import datetime
import logging

from redis_log_handler.RedisLogHandler import RedisLogHandler
from skidward.models import db, Job, JobStatus
import worker_detector


class TaskRunner:
    def update_job_status(self, job, status):
        job.query.update({"state": status})
        db.session.commit()

    def create_new_job(self, task):
        job = Job(
            state=JobStatus.RUNNING, ran_at=datetime.datetime.utcnow(), task_id=task.id
        )
        db.session.add(job)
        db.session.commit()
        logging.info("Job id:{} created".format(job.id))
        return job

    def start(self, task):
        worker_name = task.worker.name
        context = task.context

        # could get channel from context .ie {'LOGGING_CHANNEL' : "ch:channel"}
        log_handler = RedisLogHandler(context["LOGGING_CHANNEL"])
        logging.basicConfig(handlers=(log_handler,), level=logging.INFO)

        logging.info("Logging {}".format(worker_name))

        job = self.create_new_job(task)
        worker_module = worker_detector.load_worker_on_namespace(worker_name)

        logging.info("{} is running".format(worker_name))

        try:
            worker_module.start(context)
            status = JobStatus.SUCCESS
        except:
            status = JobStatus.FAIL

        logging.info("Status : {}".format(status))

        self.update_job_status(job, status=status)

        log_handler.close()
