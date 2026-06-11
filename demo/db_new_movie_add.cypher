// 1. Grabbing the node describing the genre for movie to add
MATCH (scifi:Genre {name:'Sci-Fi'})

// 2. Creating new movie as well as its relationship with genre
CREATE (dune:Movie {title:'Dune 2', annee:2024})
CREATE (dune)-[:IN_GENRE]->(scifi)

// 3. Identifying people to notify
WITH dune
MATCH (dune)-[:IN_GENRE]->(g)<-[:IN_GENRE]-(other:Movie)<-[:WATCHED]-(user:Person)
WHERE other.title <> dune.title
RETURN DISTINCT user.name AS to_notify
