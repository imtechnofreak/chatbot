from py2neo import Graph, Node, Relationship, NodeSelector
from datetime import datetime
import os

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url + '/db/data/', username=username, password=password, bolt=False, auth=False)

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.graph = graph
        self.selector = NodeSelector(graph)
        
    def find(self):
        user = self.selector.select("User", user_id=self.user_id)
        return list(user)
    
    def get_friends(self):
        query = '''
        MATCH (u:User {user_id: {user_id}})-[:FRIEND]->(f:Person)
        RETURN f
        '''
        friends = graph.run(query, user_id=self.user_id)
        return list(friends)
    
    def find_most_discussed_topic(self):
        query = '''
        MATCH(m:Message {user_id: {user_id}})
        RETURN distinct m.topic, count(*) as occurences ORDER BY occurences DESC
        '''
        topics = graph.run(query, user_id=self.user_id)
        return list(topics)
    
    def find_recent_topic(self):
        query = '''
        MATCH(m:Message {user_id: {user_id}})
        RETURN m.topic, m.last_query as last_query ORDER BY last_query DESC
        '''
        topics = graph.run(query, user_id=self.user_id)
        return list(topics)

    def find_message_by_sentiment(self):
        query = '''
        MATCH(m:Message {user_id: {user_id}})
        RETURN m, m.sentiment ORDER BY m.sentiment DESC
        '''
        messages = graph.run(query, user_id=0)
        return list(messages)
    
    def suggest_friends_by_interest(self):
        query = '''
        MATCH (p1:Person)-[:LIKES]->(hobby1)<-[:LIKES]-(p2:Person),
              (p3:Person)-[:LIKES]->(hobby1)
        WHERE p1.person_id = {user_id}
        AND NOT (p2)-[:FRIEND]->(p3)
        RETURN p2, p3
        '''
        friends = graph.run(query, user_id=0)
        return list(friends)
    
    def find_most_recent_friend(self):
        query = '''
        MATCH(u:User {user_id: {user_id}})-[]->(f:Person)
        RETURN f, f.first_mention as first_mention ORDER BY first_mention DESC
        '''
        friends = graph.run(query, user_id=0)
        return list(friends)
        
    def suggest_friends_by_location(self, city):
        query = '''
        MATCH (p1:Person), (p2:Person)
        WHERE p1.location = p2.location = {location}
        AND NOT (p1)-[:FRIEND]->(p2)
        AND p1.person_id <> p2.person_id
        RETURN p1, p2
        '''
        friends = graph.run(query, location=city)
        return list(friends)
    
    def find_events(self):
        query = '''
        MATCH (p1:Person)-[:ATTENDED]->(e:Event)
        return p1, e

        '''
        events = graph.run(query, user_id=0)
        return list(events)

    def get_node_count(self):
        query = '''
        MATCH (n)
        RETURN count(n)
        '''

    def get_relationship_count(self):
        query = '''
        MATCH ()-->()
        RETURN count(*)
        '''