#!/usr/bin/env python3
import psycopg2

DBNAME = "news"

# Given Question in udacity project"
ques1 = "Q1. What are the most popular three articles of all time?"
ques2 = "Q2. Who are the most popular article authors of all time?"
ques3 = "Q3. On which days did more than 1% of requests lead to errors?"

# sql code for question 1.
query1 ='''select a.title, count(l.id) as views
    from articles a join log l
    on l.path like concat('%',a.slug)
    group by a.title,l.path
    order by views desc limit 3;
    '''

# sql code for question 2.
query2 ='''select a.name, count(l.id) as views
    from authors a join articles ar
    on a.id = ar.author
    join log l
    on l.path like concat('%',ar.slug)
    group by a.name
    order by views desc
    '''

# sql code for question 3.
# create view with all status.
query3a = '''
    create or replace view all_data as
    select date(time), count(*) as i
    from log
    group by date(time);
'''

# create view with error status.
query3b = '''
    create or replace view all_data1 as
    select date(time), count(*) as j
    from log
    where status != '200 OK'
    group by date(time);
'''

# create view for percentage.
query3c ='''
    create or replace view all_data2 as
    select a.date, round(b.j * 100.0 / a.i, 2) as error
    from all_data as a
    join all_data1 as b
    on a.date = b.date;
    '''
    
query3 ='''
    select * from all_data2 where error > 1;
    '''

# return most three articles of all time
def popular_article():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(query1)
  posts = c.fetchall()
  print(ques1)
  for i in posts:
      print('\t"{title}" - {count} views'.format(title=i[0], count=i[1]))

  print(' ')
  db.close()
  return
      
# return most popular authors of all time
def popular_authors():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(query2)
  posts1 = c.fetchall()
  print(ques2)
  for i in posts1:
      print('\t{author} - {count} views'
              .format(author=i[0], count=i[1]))
  print(' ')
  db.close()
  return

# return above 1% request lead of error.
def above_error():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(query3a)
  c.execute(query3b)
  c.execute(query3c)
  db.commit()
  c.execute(query3)
  posts2 = c.fetchall()
  print(ques3)
  for i in posts2:
      print('\t{date} - {error}% errors'
              .format(date=i[0], error=i[1]))
  print(' ')
  db.close()
  return

popular_article()
popular_authors()
above_error()
