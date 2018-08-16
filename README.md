### #
### CREATE VIEW to sort articles and their authors and ordered by accesses count.
### #

news=> create view populars as select articles.title, authors.name, count(articles.title) as num from articles, authors, log where log.status = '200 OK' and log.path like '/article/'||articles.slug and articles.author = authors.id group by articles.title, authors.name;
CREATE VIEW

news=> select * from populars;
               title                |          name          | num
------------------------------------+------------------------+--------
 Trouble for troubled troublemakers | Rudolf von Treppenwitz |  84810
 There are a lot of bears           | Ursula La Multa        |  84504
 Balloon goons doomed               | Markoff Chaney         |  84557
 Bears love berries, alleges bear   | Ursula La Multa        | 253801
 Goats eat Google's lawn            | Ursula La Multa        |  84906
 Media obsessed with bears          | Ursula La Multa        |  84383
 Bad things gone, say good people   | Anonymous Contributor  | 170098
 Candidate is jerk, alleges rival   | Rudolf von Treppenwitz | 338647
(8 rows)


### #
### Question 1: use the view to access the 3 most accessed articles.
### #
news=> select title, num from popular order by num desc limit 3;
              title               | num
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)


### #
### Question 2: use the view to access the most popular authors.
### #
news=> select name, sum(num) as total from popular group by name order by sum(num) desc;
          name          |  total
------------------------+--------
 Ursula La Multa        | 507594
 Rudolf von Treppenwitz | 423457
 Anonymous Contributor  | 170098
 Markoff Chaney         |  84557
(4 rows)


### # 
### Question 3: create a subquery to group log.time by days, then count total accesses and errors. Then select those days with more than 1% errors.
### #

news=> SELECT to_char(log.time, 'Mon DD, YYYY'), (cast(count(status) filter (where status not like '200 OK') as decimal) / cast(count(status) as decimal) * 100) as perc FROM log GROUP BY 1;
   to_char    |          perc
--------------+------------------------
 Jul 01, 2016 | 0.70791887353055160800
 Jul 02, 2016 | 0.70471014492753623200
 Jul 03, 2016 | 0.73087157802646447700
 Jul 04, 2016 | 0.69212975611533067400
 Jul 05, 2016 | 0.77493816982687551500
 Jul 06, 2016 | 0.76678716179209113800
 Jul 07, 2016 | 0.65765436609426379200
 Jul 08, 2016 | 0.75884104277104059300
 Jul 09, 2016 | 0.74226953436164820000
 Jul 10, 2016 | 0.68087136853309842400
 Jul 11, 2016 | 0.73949024716956896700
 Jul 12, 2016 | 0.68017286967304290700
 Jul 13, 2016 | 0.69409206234142805400
 Jul 14, 2016 | 0.69389086165664178600
 Jul 15, 2016 | 0.74233106509952330700
 Jul 16, 2016 | 0.68626371609967338300
 Jul 17, 2016 | 2.26268624680272595600
 Jul 18, 2016 | 0.67279497742359099800
 Jul 19, 2016 | 0.78242171265427079400
 Jul 20, 2016 | 0.70201807284124860200
 Jul 21, 2016 | 0.75668434677141977900
 Jul 22, 2016 | 0.73542730862587399900
 Jul 23, 2016 | 0.67949138339344919300
 Jul 24, 2016 | 0.78221415607985480900
 Jul 25, 2016 | 0.71594675260469119100
 Jul 26, 2016 | 0.72823568354849387600
 Jul 27, 2016 | 0.67353043733597606900
 Jul 28, 2016 | 0.71719254703724656500
 Jul 29, 2016 | 0.69516478317046095600
 Jul 30, 2016 | 0.72086140213897917300
 Jul 31, 2016 | 0.71763551096084633000
(31 rows)


news=> SELECT err_perc FROM (SELECT to_char(log.time, 'Mon DD, YYYY'), cast(count(status) filter (where status not like '200 OK') as decimal) / cast(count(status) as decimal) * 100 as err_perc FROM log GROUP BY 1) AS err_query WHERE err_perc > 1.0;
        err_perc
------------------------
 2.26268624680272595600
(1 row)

### #
### Program result:
### #

vagrant@vagrant:/vagrant/logs_analysis$ python log_analysis.py
1. What are the most popular three articles of all time?
        Candidate is jerk, alleges rival -- 338647 views.
        Bears love berries, alleges bear -- 253801 views.
        Bad things gone, say good people -- 170098 views.


2. Who are the most popular article authors of all time?
        Ursula La Multa -- 507594 views.
        Rudolf von Treppenwitz -- 423457 views.
        Anonymous Contributor -- 170098 views.
        Markoff Chaney -- 84557 views.


3. On which days did more than 1% of requests lead to errors?
        Jul 17, 2016 -- 2.26268624680272595600% errors.
