from pipeline.intitalTrain_pipeline import run_initial_training_pipeline
from pipeline.dailyUpdate_pipeline import daily_update_job
from apscheduler.schedulers.blocking import BlockingScheduler


def start_pipeline():
    # print("Starting initial training pipeline...")
    # run_initial_training_pipeline()

    print("Scheduling daily update job...")
    scheduler = BlockingScheduler()
    scheduler.add_job(daily_update_job, "cron", hour=12, minute=12)
    print("Scheduler started. Waiting for next run...")

    scheduler.start()


if __name__ == "__main__":
    start_pipeline()
