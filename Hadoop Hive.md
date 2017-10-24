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

Results:
 - 273 Females
 - 670 Males

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

| occupation    | gender | _c0 | 
|---------------|--------|-----| 
| administrator | F      | 36  | 
| administrator | M      | 43  | 
| artist        | F      | 13  | 
| artist        | M      | 15  | 
| doctor        | M      | 7   | 
| educator      | F      | 26  | 
| educator      | M      | 69  | 
| engineer      | F      | 2   | 
| engineer      | M      | 65  | 
| entertainment | F      | 2   | 
| entertainment | M      | 16  | 
| executive     | F      | 3   | 
| executive     | M      | 29  | 
| healthcare    | F      | 11  | 
| healthcare    | M      | 5   | 
| homemaker     | F      | 6   | 
| homemaker     | M      | 1   | 
| lawyer        | F      | 2   | 
| lawyer        | M      | 10  | 
| librarian     | M      | 22  | 
| librarian     | F      | 29  | 
| marketing     | F      | 10  | 
| marketing     | M      | 16  | 
| none          | F      | 4   | 
| none          | M      | 5   | 
| other         | F      | 36  | 
| other         | M      | 69  | 
| programmer    | F      | 6   | 
| programmer    | M      | 60  | 
| retired       | F      | 1   | 
| retired       | M      | 13  | 
| salesman      | F      | 3   | 
| salesman      | M      | 9   | 
| scientist     | F      | 3   | 
| scientist     | M      | 28  | 
| student       | F      | 60  | 
| student       | M      | 136 | 
| technician    | F      | 1   | 
| technician    | M      | 26  | 
| writer        | F      | 19  | 
| writer        | M      | 26  | 


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

| Gender | Avgrating | Title                                             | 
|--------|-----------|---------------------------------------------------| 
| F      | 5.0       | Stripes (1981)                                    | 
| F      | 5.0       | Foreign Correspondent (1940)                      | 
| F      | 5.0       | Year of the Horse (1997)                          | 
| F      | 5.0       | Telling Lies in America (1997)                    | 
| M      | 5.0       | They Made Me a Criminal (1939)                    | 
| F      | 5.0       | Everest (1998)                                    | 
| F      | 5.0       | Someone Else's America (1995)                     | 
| M      | 5.0       | "Quiet Room, The (1996)"                          | 
| M      | 5.0       | Entertaining Angels: The Dorothy Day Story (1996) | 
| M      | 5.0       | "Great Day in Harlem, A (1994)"                   | 
| M      | 5.0       | Hugo Pool (1997)                                  | 
| M      | 5.0       | Prefontaine (1997)                                | 
| M      | 5.0       | "Letter From Death Row, A (1998)"                 | 
| M      | 5.0       | Marlene Dietrich: Shadow and Light (1996)         | 
| M      | 5.0       | Little City (1998)                                | 
| M      | 5.0       | Santa with Muscles (1996)                         | 
| M      | 5.0       | Star Kid (1997)                                   | 
| M      | 5.0       | Delta of Venus (1994)                             | 
| M      | 5.0       | Aiqing wansui (1994)                              | 
| F      | 5.0       | Maya Lin: A Strong Clear Vision (1994)            | 
| M      | 5.0       | Love Serenade (1996)                              | 
| F      | 5.0       | Faster Pussycat! Kill! Kill! (1965)               | 
| M      | 5.0       | "Leading Man, The (1996)"                         | 
| F      | 5.0       | Prefontaine (1997)                                | 
| F      | 5.0       | Mina Tannenbaum (1994)                            | 
| F      | 5.0       | "Visitors, The (Visiteurs, Les) (1993)"           | 
| M      | 5.0       | "Saint of Fort Washington, The (1993)"            | 
