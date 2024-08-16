### WIP

# import asyncio
# import datetime
# import pytest

# from app.background import BackgroundRunner
# from app.database import AsyncSessionLocal, SessionLocal, engine
# from app.models.base import Base
# from app.models.appointments import Appointment
# from app.models.providers import Provider

# pytest_plugins = ('pytest_asyncio',)


# @pytest.fixture(scope="module", autouse=True)
# def setup_database():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture(scope="module", autouse=True)
# async def background_runner():
#     runner = BackgroundRunner(db=SessionLocal, sleep_time=1)
#     await asyncio.create_task(runner.run_main())
#     yield runner


# @pytest.mark.asyncio
# async def test_background_runner_remove_expired_appointments(background_runner):
#     with SessionLocal() as session:
#         provider = Provider(first_name="John", last_name="Smith")
#         appointment1 = Appointment(
#             provider_id=provider.id,
#             booked_time=datetime.datetime.now() - datetime.timedelta(minutes=60)
#         )
#         appointment2 = Appointment(
#             provider_id=provider.id,
#             booked_time=datetime.datetime.now() - datetime.timedelta(minutes=20)
#         )
#         session.add(provider)
#         session.add(appointment1)
#         session.add(appointment2)
#         session.commit()
    
#     await asyncio.sleep(3)

#     with SessionLocal() as session:
#         appointments = session.query(Appointment).all()

#         assert appointments[0].booked_time is not None
#         assert appointments[1].booked_time is None
