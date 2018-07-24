# General queries that the chatbot can make

Find all users in the system:

> MATCH(u:User) RETURN u

Find all of user0's friends (should the relation be directional?):

> MATCH(u:User {user_id: 0})-[:FRIEND]->(f:Person) RETURN f

Find the topics that user0 most discussed:

> MATCH(m:Message {user_id: 0})
> RETURN distinct m.topic, count(*) as occurences ORDER BY occurences DESC

Find friends with similar interests that don't know eachother

> MATCH (p1:Person)-[:LIKES]->(hobby1)<-[:LIKES]-(p2:Person),
> (p3:Person)-[:LIKES]->(hobby1)
> where p1.person_id = 0
> AND NOT (p2)-[:FRIEND]->(p3)
> RETURN p2, p3

Find most recent person mentioned

> MATCH(u:User {user_id: 0})-[]->(f:Person)
> RETURN f, f.first_mention as first_mention ORDER BY first_mention DESC

Find people living in the same location that don't know eachother

> MATCH (p1:Person), (p2:Person)
> WHERE p1.location = p2.location = "Waterloo"
> AND NOT (p1)-[:FRIEND]->(p2)
> AND p1.person_id <> p2.person_id
> RETURN p1, p2

Find people that attended an event

> MATCH (p1:Person)-[:ATTENDED]->(e:Event)
> return p1, e

Find the most recent topics:

> MATCH(m:Message {user_id: 0})
> RETURN m.topic, m.last_query as last_query ORDER BY last_query DESC

Find the messages that resulted in the highest sentiment:

> MATCH(m:Message {user_id: 0})
> RETURN m, m.sentiment ORDER BY m.sentiment DESC

## TODO: Need to think more about the following possible queries

* Find person that was most mentioned
* Find cycle that resulted in a negative sentiment
* Discover possible topic conversations (recommendations?)