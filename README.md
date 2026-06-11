# Overview

This repository holds a small study on no-SQL modelling paradigms.

It is structured over the following files.
Note that apart from this small README, all content is in French.

# Project structure (French)

- Brainstorm: confer https://mensuel.framapad.org/p/hb__2026-06__pld_nosql-alrl?lang=fr
- Code: confer demo (confer how to run section)
- Summary: confer "Le modèle Graph: brève présentation : principes, forces et faiblesses, cas d'usage"
- Presentation slides: confer "Graph: un concept, 5 slides"

# Demo - How to run

You must have the following tools installed on your system.
- Docker
- Python3 with neo4j integration library.
- any Command Line Interface (ex Bash on GNU/Linux distributions).
Then set up a docker container with a predefined sample Neo4j database
```docker run --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password -d neo4j:latest```

Then, place yourself in the `./demo` section and run the following:
    `python3 neo4j_demo.py`
