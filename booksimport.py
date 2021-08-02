import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import BookDetails

engine = create_engine('postgresql://gkuevkgkttisvm:3837757d6a34f1762ceafc9a2d3ee7af6aa2776c45890bd21c8be9c7238d3082@ec2-52-45-183-77.compute-1.amazonaws.com:5432/d397aj7gdd13fg')
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

