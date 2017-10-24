# Hadoop Hive
Hadoop is a kind of database for big data.
It acts as a distributed filesystem with HDFS and executes Map and Reduce actions on the data.

Hive is a tool on top of Hadoop. It gives an SQL-like interface to the database.
It converts the SQL statements to map and reduce actions.

# Some examples
I will give some examples using a dataset of iMDB.

# Creating the tables
Creating the userdata table. Other tables are similar.
```SQL
CREATE TABLE userdata (
  userid int,
  itemid int,
  rating float,
  stamp int
  )
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
```
To load the data, the following query needs to be executed"
```SQL
LOAD DATA INPATH '/user/root/assignment4/u.data' OVERWRITE INTO TABLE userdata;
```

After this you can query the userdata table for the data of movies.

# The number of Male and Female users
This is quite easy to use. You can't all users and group them by gender.

In Map Reduce terms this is mapping on gender and one, and reducing by counting per gender.

Example query:
```SQL
SELECT COUNT(*), gender FROM users GROUP BY gender;
```

# The number of Male and Female users grouped by occupation
This a step more difficult than the first query, but uses the same principle.
You use in another group by.

In Map Reduce therms this is extending the map with occupation, and reducing on two parts.

Example query:
```SQL
SELECT COUNT(*), occupation, gender 
FROM users 
GROUP BY occupation, gender 
ORDER BY occupation;
```

# The highest rated movie per gender
Here we map users to their votes and votes to their movies. Then we reduce the votes to counts per movie per gender.
We order that result and only give the highest values in the result set.

A subquery is required because of the working of the groupby query. 

Example query:
```SQL
SELECT t.gender, t.avgrating, i.title FROM 
  (SELECT u.gender AS gender, AVG(d.rating) AS avgrating, i.id AS movieid, rank() OVER (ORDER BY AVG(d.rating) DESC) AS r
   FROM users u, useritem i, userdata d 
   WHERE u.userid = d.userid 
   AND d.itemid = i.id 
   GROUP BY u.gender, i.id) AS t,
useritem AS i
WHERE t.movieid = i.id
AND t.r = 1;
```

