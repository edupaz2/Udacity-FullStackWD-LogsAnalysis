#!/usr/bin/env python
# 
# log_analysis.py -- implementation for Log Analysis project
#

import psycopg2

def run():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    
    # Create a view for most popular articles with their authors, removing failures (log.status) and not proper paths (/article/...)
    #c.execute("create view popular_articles as select path, count(*) as num from log where status = '200 OK' and path like '/article/%' group by path order by num desc")
    view = "CREATE VIEW populars AS \
    		SELECT articles.title, authors.name, count(articles.title) as num \
    		FROM articles, authors, log \
    		WHERE log.status = '200 OK' AND log.path LIKE '/article/'||articles.slug AND articles.author = authors.id \
    		GROUP BY articles.title, authors.name"
    c.execute(view)
    db.commit()

    ### Query 1 ###
    query = "SELECT \
    			title, num \
    		FROM populars \
    		ORDER BY num DESC \
    		LIMIT 3"
    c.execute(query)
    results = c.fetchall()

    print('1. What are the most popular three articles of all time?')
    for r in results:
    	print('\t' + r[0] + ' -- ' + str(r[1]) + ' views.')
    print('\n')

    ### Query 2 ###
    query = "SELECT \
    			name, \
    			sum(num) as total \
    		FROM populars \
    		GROUP BY name \
    		ORDER BY total DESC"
    c.execute(query)
    results = c.fetchall()

    print('2. Who are the most popular article authors of all time?')
    for r in results:
    	print('\t' + r[0] + ' -- ' + str(r[1]) + ' views.')
    print('\n')

    # Remove view
    c.execute("drop view populars")
    db.commit()

    ### Query 3 ###
    query = "SELECT day, err_perc FROM \
    			(SELECT \
    				to_char(log.time, 'Mon DD, YYYY') AS day, \
    				cast(count(status) filter (where status not like '200 OK') as decimal) / cast(count(status) as decimal) * 100 AS err_perc \
    			FROM log \
    			GROUP BY 1) \
    		AS err_query \
    		WHERE err_perc > 1.0"

    c.execute(query)
    results = c.fetchall()

    print('3. On which days did more than 1% of requests lead to errors?')
    for r in results:
    	print('\t' + r[0] + ' -- ' + str(r[1]) + '% errors.')
    print('\n')

    db.close()

if __name__ == '__main__':
  run()
