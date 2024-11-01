from aiogram import Bot
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.group_handlers import create_new_form, get_needed_forms


class Scheduler:
    scheduler = None
    bot = None

    start_time = None
    end_time = None

    def __init__(self, bot: Bot):
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.bot = bot

        self.scheduler.add_job(self.new_season,
                               trigger="date",
                               run_date=datetime(datetime.now().year, 9, 2, 13, 0, 0)
                               )

        self.scheduler.add_job(self.new_season,
                               trigger="date",
                               run_date=datetime(datetime.now().year, 1, 6, 13, 0, 0)
                               )

        self.scheduler.start()

    async def new_season(self):
        # create_sheet()
        await self.set_start_end_dates()
        for job in self.scheduler.get_jobs():
            if job.id == "analyze_needed_forms" or job.id == "creating_form":
                self.scheduler.remove_job(job_id=job.id)
        await self.set_schedulers()

    async def set_schedulers(self):
        self.scheduler.add_job(create_new_form,
                               trigger="interval",
                               days=14,
                               start_date=self.start_time,
                               end_date=self.end_time,
                               id="creating_form",
                               args=[self.bot]
                               )

        self.scheduler.add_job(get_needed_forms,
                               trigger="interval",
                               days=14,
                               start_date=self.start_time,
                               end_date=self.end_time,
                               id="analyze_needed_forms",
                               args=[self.bot]
                   )

    """
    Расчет нового времени начала и остановки в два вида сезона
    START_DATE_AUTUMN_WINTER - первый понедельник с 1 сен
    END_DATE_AUTUMN_WINTER - последний понедельник когда все дни недели еще в этом году

    START_DATE_WINTER_SPRING - первый понедельник после 7 янв
    END_DATE_WINTER_SPRING - до марта
    """

    async def set_start_end_dates(self):
        pass
    #     if datetime.now().month <:
    #         self.start_time = datetime()
    #         self.end_time = datetime()
    #     else:
    #         self.start_time = datetime()
    #         self.end_time = datetime()

    async def shutdown(self):
        self.scheduler.shutdown()
