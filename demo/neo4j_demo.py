from neo4j import GraphDatabase

# Bolt: custom, proprietary protocol designed by Neo4j for its Cypher DML.
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# Create nodes and relationship
with driver.session() as session:
    session.run("CREATE (:Person {name:$name1})-[:FRIENDS_WITH]->(:Person {name:$name2})",
                name1="Alice", name2="Bob")

# Query friends
with driver.session() as session:
    result = session.run(
        "MATCH (a:Person)-[:FRIENDS_WITH]->(friend) WHERE a.name=$name RETURN friend.name",
        name="Alice"
    )
    for record in result:
        print(record[0])

# Clean up
driver.close()  # this is pseudocode; close the driver at the end of your script
