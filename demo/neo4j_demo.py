from neo4j import GraphDatabase

# Bolt: custom, proprietary protocol designed by Neo4j for its Cypher DML.

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password"
INIT_FILE = "db_initial_populate.cypher"
ADD_FILE = "db_new_movie_add.cypher"

def init_demo_state_from_file(filename=INIT_FILE, uri=URI):
    print("=== Neo4j demo: Setting up content ====")
    print("Warning: all previous data will be erased")
    # 1. Opening up "instructions's source file"
    with open(filename, 'r', encoding='utf-8') as file:
        CYPHER_QUERY = file.read()
    try:
        with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
            
            # Étape 1 : "Truncate"
            print("1. Removing all existing data")
            with driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                print("   -> Db emptied successfully")
            
            # Étape 2 : Exécuter la création et récupérer les résultats
            print("2. Inserting initial data...")
            with driver.session() as session:
                result = session.run(CYPHER_QUERY)
                print("\n--- Initial data inserted successfully")

    except Exception as e:
        print(f"Error occurred : {e}")


def add_movie_and_notify(filename=ADD_FILE, uri=URI):
    print("=== Neo4j demo: Adding a new movie (Dune2, scifi) ====")
    print("Should trigger a notification for people liking the genre")
    # 1. Opening up "instructions's source file"
    with open(filename, 'r', encoding='utf-8') as file:
        CYPHER_QUERY = file.read()
    try:
        with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
            with driver.session() as session:
                result = session.run(CYPHER_QUERY)
                
                print("\n--- People to notify for 'DUNE 2' ---")
                # Parcours des résultats retournés par le RETURN de la requête Cypher
                for record in result:
                    print(f"- {record['to_notify']}")
                print("-------------------------------------------------------")

    except Exception as e:
        print(f"Error occurred : {e}")

init_demo_state_from_file(INIT_FILE)
add_movie_and_notify(ADD_FILE)
