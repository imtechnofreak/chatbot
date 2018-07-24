LOAD CSV WITH HEADERS FROM "file:///users.csv" AS row
MERGE (n:User {user_id: toInteger(row.user_id)})
ON CREATE SET n = row,
	n.user_id = toInteger(row.user_id),
    n.name = row.name,
    n.location = row.location,
    n.age = toInteger(row.age),
    n.gender = row.gender,
    n.created_at = timestamp()
ON MATCH SET 
    n.last_query = timestamp()
;
LOAD CSV WITH HEADERS FROM "file:///people.csv" AS row
MERGE (n:Person {person_id: toInteger(row.person_id)})
ON CREATE SET n = row,
	n.person_id = toInteger(row.person_id),
    n.name = row.name,
    n.location = row.location,
    n.age = toInteger(row.age),
    n.gender = row.gender,
    n.first_mention = timestamp()
ON MATCH SET
    n.last_mention = timestamp()
;

LOAD CSV WITH HEADERS FROM "file:///relationships.csv" AS row
MATCH (u:User {user_id: toInteger(row.user_id)}), (p:Person {person_id: toInteger(row.person_id)})
FOREACH(n IN CASE WHEN trim(row.relationship) = "friend" THEN [1] ELSE [] END | MERGE (u)-[:FRIEND]->(p))
FOREACH(n IN CASE WHEN trim(row.relationship) = "cousin" THEN [1] ELSE [] END | MERGE (u)-[:COUSIN]->(p))
FOREACH(n IN CASE WHEN trim(row.relationship) = "mom" THEN [1] ELSE [] END | MERGE (u)-[:MOM]->(p))
FOREACH(n IN CASE WHEN trim(row.relationship) = "dad" THEN [1] ELSE [] END | MERGE (u)-[:DAD]->(p))
;

LOAD CSV WITH HEADERS FROM "file:///messages.csv" AS row
MERGE (u:User {user_id: toInt(row.user_id)})
MERGE (p:Message {message_id: toInt(row.message_id)})
ON CREATE SET
	p = row,
    p.sentiment = toInt(row.sentiment),
    p.message_id = toInt(row.message_id),
    p.previous_id = toInt(row.previous_id),
    p.created_at = timestamp()
ON MATCH SET
	p.last_query = timestamp()    

MERGE (c:Message {message_id: toInt(row.previous_id)})
ON CREATE SET
	c = row,
    c.sentiment = toInt(row.sentiment),
    c.message_id = toInt(row.message_id),
    c.previous_id = toInt(row.previous_id)
ON MATCH SET
	c.last_query = timestamp()

FOREACH(n IN CASE WHEN row.message_id <> row.previous_id THEN [1] ELSE [] END | MERGE (c)-[r:FOLLOWED_BY]->(p))
FOREACH(n IN CASE WHEN row.message_id = row.previous_id THEN [1] ELSE [] END | MERGE (u)-[:STARTED]->(p));