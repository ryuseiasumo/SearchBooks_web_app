#データベースのリセット
import os
if os.path.exists('project/db.sqlite'):
    os.remove('project/db.sqlite')

from project import db, create_app
db.create_all(app=create_app())



#Aozoraテーブルにcsvファイルの内容を収録
import pandas as pd
from project.models import Aozora
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
engine = create_engine('sqlite:///project/db.sqlite')
session = Session(bind = engine)

try:
    file_name= "./project/csv/aozora.csv"
    csv_data=pd.read_csv(file_name)
    csv_data=csv_data.values.tolist()

    cnt = 1
    for row in csv_data:
        record= Aozora(**{
            'id' : cnt,
            'book_id' : row[0],
            'title' : row[1].replace('\u3000', ' '),
            'author' : row[2].replace('\u3000', ' '),
            'shuroku' : str(row[3]).replace('\u3000', ' '),
            'publisher' : str(row[4]).replace('\u3000', ' ')
        })
        session.add(record)
        cnt += 1
    session.commit()
except:
    session.rollback() #Rollback the changes on error
finally:
    session.close() #Close the connection


for aozora in session.query(Aozora):
    print("{} - {} {} {} {} {}".format(aozora.id, aozora.book_id, aozora.title, aozora.author, aozora.shuroku, aozora.publisher))


# all_staffs = session.query(Aozora).all()
# print(all_staffs)

# for aozora in session.query(Aozora).order_by(Aozora.id):
#     print("{} - {}".format(aozora.id, aozora.title))

# print(session.query(Aozora.id, Aozora.book_id, Aozora.title, Aozora.author).all())
