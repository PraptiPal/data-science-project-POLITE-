from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

today = datetime.strftime(datetime.today(), '%d/%M/%y')

Base = declarative_base()


class Search(Base):

    __tablename__ = "searches"

    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    date = Column(String, default=today)
    sentiment = Column(String)
    subjectivity = Column(String)


if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)
