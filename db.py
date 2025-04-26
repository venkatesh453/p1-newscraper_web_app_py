from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    published_date = Column(String)
    summary = Column(Text)
    html_content = Column(Text)

engine = create_engine('sqlite:///news.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

#update
