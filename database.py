from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgres://whatsautodb_user:9VVfAXKuQzO4RYYbtOMds4AyFtj43LsT@dpg-cphhlau3e1ms73d8kqh0-a/whatsautodb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    app = Column(String, index=True)
    sender = Column(String, index=True)
    message = Column(Text)
    group_name = Column(String, index=True)
    phone = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    prevstatus = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
