import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), echo=False)
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    completed = Column(Boolean)
    last_word = Column(String)

    def __repr__(self):
        return f"TaskID: {self.id}\n" \
               f"\tCompleted: {self.completed}\n" \
               f"\tLast word: {self.last_word}"


class SearchResult(Base):

    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'))
    word = Column(String)
    result = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
