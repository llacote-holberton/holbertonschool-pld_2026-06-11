# Overview

This repository holds a small study on no-SQL modelling paradigms.

It is structured over the following files.
Note that apart from this small README, all content is in French.

# Project structure (French)

- Brainstorm: just structured notes.
- Code: confer demo (confer how to run section)
- Summary: confer [Le modèle Graph: brève présentation : principes, forces et faiblesses, cas d'usage](summary.md)
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

# Brainstorm
Live document with view of each teammate's contribution can be seen hereunder.
<iframe name="embed_readonly" src="https://mensuel.framapad.org/p/r.ecff5d15dc97aff19b6af3560134be1e?showControls=true&showChat=true&showLineNumbers=true&useMonospaceFont=false" width="100%" height="600" frameborder="0"></iframe>


The raw source is stored for archivage in [brainstorm.md](brainstorm.md) (as the original framapad [hb__2026-06__pld_nosql-alrl](https://mensuel.framapad.org/p/hb__2026-06__pld_nosql-alrl?lang=fr) will be automatically deleted on July 12th).

# LICENSE and AUTHORS
Work published under [CC-By-SA license](https://creativecommons.org/licenses/by-sa/4.0/).

Authors:
- Soufiane Filali
- Laurent Lacôte
- Noham Oulma
