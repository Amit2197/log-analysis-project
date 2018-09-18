
# Log Analysis Project

*create a reporting tool that prints out reports (in plain text)
based on the data in the database. This reporting tool is a
Python program using the psycopg2 module to connect to the database.*

## Content Of Table
* [Introduction](#introduction)
* [Installation and Setup](#installation)
* [Create Views](#create-views)

# Introduction
This is the solution for the Logs Analysis project in Udacity Full Stack Nanodegree course. In this, we have to execute complex queries on a large database (> 1000k rows) to extract intersting stats.

The database in question is a newspaper company database where we have 3 tables; articles, authors and log.

articles - Contains articles posted in the newspaper so far.  
authors - Contains list of authors who have published their articles.  
log - Stores log of every request sent to the newspaper server.  
This project implements a single query solution for each of the question in hand. See [newsdata.py]() for more details.

# Installation
1. Install [virtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/).
2. open terminal and type following command

    1. clone repository from github  
    > `git clone https://github.com/Amit2197/log-analysis-project.git`

    2. type <strong>cd log-analysis-project</strong>
    > `cd log-analysis-project`

    3. type vagrant up and vagrant ssh
    >`vagrant up`  
    >`vagrant ssh`

    4. Go to another directory vagrant type
    >`cd /Vagrant`

    5. Now, run newsdata.py as,
    >`python3 newsdata.py`

    ```
    Output :  

      1. What are the most popular three articles of all time?
        "Candidate is jerk, alleges rival" - 338647 views
        "Bears love berries, alleges bear" - 253801 views
        "Bad things gone, say good people" - 170098 views

      2. Who are the most popular article authors of all time?
         Ursula La Multa - 507594 views
         Rudolf von Treppenwitz - 423457 views
         Anonymous Contributor - 170098 views
         Markoff Chaney - 84557 views

      3. On which days did more than 1% of requests lead to errors?
         2016-07-17 - 2.26% errors
    ```

# Create views

  ```
    create or replace view all_data as
    select date(time), count(*) as i
    from log
    group by date(time);
  ```

  ```
    create or replace view all_data1 as
    select date(time), count(*) as j
    from log
    where status != '200 OK'
    group by date(time);
  ```

  ```
    create or replace view all_data2 as
    select a.date, round(b.j * 100.0 / a.i, 2) as error
    from all_data as a
    join all_data1 as b
    on a.date = b.date;
  ```
