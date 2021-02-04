from discord_ritoman.db.schema import Base
from discord_ritoman.db.session import postgresql_engine, session as db_session


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    Base.metadata.create_all(postgresql_engine)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    db_session.commit()
    Base.metadata.drop_all(postgresql_engine)
