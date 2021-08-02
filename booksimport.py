import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import BookDetails

engine = create_engine(os.getenv('HEROKU_DB_URL'))
db_session = scoped_session(sessionmaker(bind=engine))
with open('books.csv') as csvfile:
    records = list(csv.reader(csvfile,delimiter=','))
    for row in records[1:]:
        # print(int(row[3]))
        new = BookDetails(isbn=row[0],
                          title = row[1],
                          author=row[2],
                          year=int(row[3]))
        db_session.add(new)
db_session.commit()
db_session.close()

