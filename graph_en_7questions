# Neo4j — Base de données graphe

**Holberton School France — Trimestre 2 — Juin 2026**

---

## Sommaire

1. [C'est quoi ce modèle, et pourquoi existe-t-il ?](#1-cest-quoi-ce-modèle-et-pourquoi-existe-t-il-)
2. [Comment les données sont-elles représentées ?](#2-comment-les-données-sont-elles-représentées-)
3. [Comment fonctionnent les opérations de base (CRUD) ?](#3-comment-fonctionnent-les-opérations-de-base-crud-)
4. [Quels sont les cas d'usage ?](#4-quels-sont-les-cas-dusage-)
5. [Quels compromis ou limites ?](#5-quels-compromis-ou-limites-)
6. [Comment se compare-t-il au relationnel ?](#6-comment-se-compare-t-il-au-relationnel-)
7. [Place dans une architecture polyglotte](#7-place-dans-une-architecture-polyglotte-)

---

## 1. C'est quoi ce modèle, et pourquoi existe-t-il ?

Neo4j est une base de données qui stocke des **connexions entre des choses**.

Imagine Netflix — tu as des utilisateurs, des films, des genres. La question intéressante c'est pas *"liste-moi tous les films"*, c'est :

> *"Alice a regardé Inception, Bob aussi, ils se suivent, et un nouveau film Sci-Fi sort — qui notifier ?"*

Dans une base classique comme MySQL, répondre à cette question c'est des jointures dans tous les sens — lent et compliqué. Dans Neo4j tu suis juste les flèches.

Neo4j existe pour créer des applications robustes à la charge **dont le fonctionnement repose avant tout sur les relations entre les données** — réseau social, système de recommandations, détection de fraude.

---

## 2. Comment les données sont-elles représentées ?

### Les 3 éléments fondamentaux

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ( Alice )  ──────[:WATCHED {note:9}]──────>  ( Inception )│
│   :Person                                       :Movie      │
│   name:'Alice'                                  title:'...' │
│   age: 28                                       annee: 2010 │
│                                                             │
│                          │                                  │
│                   [:IN_GENRE]                               │
│                          │                                  │
│                          ▼                                  │
│                      ( Sci-Fi )                             │
│                       :Genre                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Élément | Description | Exemple |
|---|---|---|
| **Nœud** | Une entité (personne, film, ville) | `(alice:Person {name:'Alice'})` |
| **Propriété** | Une info attachée à un nœud ou une relation | `{name:'Alice', age:28}` |
| **Relation** | Un lien typé et orienté entre deux nœuds | `(alice)-[:WATCHED {note:9}]->(film)` |

### Spécificités de stockage

Neo4j utilise **4 fichiers séparés** sur le disque :

```
neostore.nodestore.db        → les nœuds
neostore.relationshipstore.db → les relations
neostore.propertystore.db    → les propriétés
neostore.labeltokenstore.db  → les labels et types
```

**Index-free adjacency** : chaque nœud stocke directement en mémoire des pointeurs physiques (liste chaînée) vers ses relations voisines. Résultat : aucune jointure, on suit juste les pointeurs.

```
Nœud Alice  →  [rel#4: WATCHED → Inception]
                    → [rel#7: WATCHED → Matrix]
                        → [rel#12: FRIENDS_WITH → Bob]
```

---

## 3. Comment fonctionnent les opérations de base (CRUD) ?

Le langage s'appelle **Cypher**.

### CREATE — Créer

Cypher propose deux méthodes :

- **`CREATE`** — crée quoi qu'il arrive, quitte à créer un doublon
- **`MERGE`** — équivalent de *"retourne l'entrée si elle existe, sinon crée-la"*

```cypher
-- Créer un nœud
CREATE (alice:Person {name:'Alice'})

-- MERGE : évite les doublons
MERGE (g:Genre {name:'Sci-Fi'})
ON CREATE SET g.popularite = 0.95
```

> ⚠️ Attention avec MERGE sur des relations : il vaut mieux d'abord s'assurer de l'existence des nœuds, puis créer la relation séparément.

### READ — Lire

`MATCH` est l'équivalent du `SELECT` SQL. Il faut toujours l'associer à un `RETURN`.

```cypher
MATCH (p:Person)-[w:WATCHED]->(m:Movie)
WHERE w.note >= 8
RETURN p.name, m.title, w.note
ORDER BY w.note DESC
```

### UPDATE — Modifier

`MATCH` pour cibler, `SET` pour modifier.

```cypher
MATCH (p:Person {name:'Alice'})
SET p.age = 30
```

### DELETE — Supprimer

- **`REMOVE`** — supprime une propriété
- **`DELETE`** — supprime une entité (uniquement si elle n'a plus de relations)
- **`DETACH DELETE`** — supprime l'entité ET toutes ses relations

```cypher
MATCH (p:Person {name:'Bob'})
DETACH DELETE p
```

### Résumé CRUD

```
CREATE / MERGE  →  INSERT INTO
MATCH + RETURN  →  SELECT FROM
MATCH + SET     →  UPDATE SET
DETACH DELETE   →  DELETE FROM
```

---

## 4. Quels sont les cas d'usage ?

Tous les services dont le traitement repose sur les **relations entre les données** :

```
Combinaison de contraintes de relations
─────────────────────────────────────────────────────────────
"Utilisateurs qui aiment les Romances ET suivent tel réalisateur
 ET ont regardé tel acteur"

Grande chaîne de relations (multi-sauts)
─────────────────────────────────────────────────────────────
"Trouve tous les gens que connaît X, que connaît Y,
 qui est le cousin de Z"
```

| Domaine | Cas concret |
|---|---|
| 🎬 Streaming | Recommandations Netflix, Spotify |
| 🏦 Finance | Détection de fraude bancaire |
| 👥 Réseau social | Suggestions d'amis LinkedIn |
| 🗺️ Cartographie | Google Maps, chemins les plus courts |
| 🔒 Cybersécurité | Analyse de propagation d'attaques |

---

## 5. Quels compromis ou limites ?

Neo4j excelle pour **suivre des relations** (chemins, recommandations, fraude) quel que soit le nombre de sauts — contrairement au SQL qui ralentit avec les jointures multiples.

| ✅ Points forts | ❌ Limites |
|---|---|
| Traversée de relations ultra-rapide | Moins efficace pour les agrégations globales (SUM, COUNT sur millions de lignes) |
| Schéma flexible | Écosystème moins mature que SQL |
| Requêtes multi-niveaux simples | Performances dépendantes de la RAM disponible |
| Pas de jointures | Moins de développeurs formés |

> En résumé : Neo4j est excellent pour les données **en réseau**, le relationnel reste meilleur pour les données **en tableau**.

---

## 6. Comment se compare-t-il au relationnel ?

```
MySQL                              Neo4j
─────────────────────────────────────────────────────────────

Table users   ←──JOIN──→  Table watched   Table users
Table movies  ←──JOIN──→  Table watched   ↕ [:WATCHED]
                                          Table movies

→ La jointure est CALCULÉE             → La relation est STOCKÉE
  à chaque requête                       une fois pour toutes
```

| Critère | MySQL | Neo4j |
|---|---|---|
| Structure | Tables, lignes, colonnes | Nœuds, relations, propriétés |
| Langage | SQL | Cypher |
| Relations profondes | Lentes (jointures recalculées) | Rapides (pointeurs directs) |
| Agrégations globales | ✅ Excellent | ⚠️ Moins adapté |
| Schéma | Fixe | Flexible |
| Maturité | ✅ Très mature | ⚠️ Plus jeune |

---

## 7. Place dans une architecture polyglotte

> La **persistance polyglotte** c'est l'usage combiné de différents paradigmes de bases de données pour profiter des points forts de chacun.

Réservé aux cas d'usage complexes : YouTube, Google Maps, Netflix, LinkedIn.

### Exemple — YouTube

```
┌──────────────────────────────────────────────────────────┐
│                      YouTube                             │
├────────────────┬──────────────────┬──────────────────────┤
│   SQL          │   Neo4j (graphe) │   Document           │
│                │                  │                      │
│ Gestion du     │ Recommandations  │ Diffusion            │
│ contenu        │                  │                      │
│                │ - titre          │ - flux vidéo brut    │
│ - statistiques │ - genre          │ - métadonnées        │
│ - durée moy.   │ - réalisateur    │ - sous-titres        │
│ - catégories   │ - acteur         │ - commentaires       │
│ - nb vues      │ - utilisateur    │                      │
└────────────────┴──────────────────┴──────────────────────┘
```

### Exemple générique

```
MySQL          →  données transactionnelles (commandes, paiements)
Neo4j          →  relations et recommandations
Redis          →  cache et sessions
Elasticsearch  →  recherche full-text
```

---

## POC — Lancer le projet

### 1. Démarrer Neo4j
```bash
docker run --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password -d neo4j:5
```

### 2. Ouvrir Neo4j Browser
```
http://localhost:7474
Login    : neo4j
Password : password
```

### 3. Exécuter le POC
Copie-coller le contenu de `poc.cypher` dans le browser et appuyer sur **Ctrl+Entrée**.

### Fonctionnalité distinctive — Recommandation par genre

Quand un nouveau film sort, trouver automatiquement les utilisateurs à notifier :

```cypher
MATCH (new:Movie {title:'Dune 2'})
      -[:IN_GENRE]->(g)<-[:IN_GENRE]-(other:Movie)
      <-[:WATCHED]-(user:Person)
WHERE other.title <> new.title
RETURN DISTINCT user.name AS a_notifier
```

---

## Sources

- Neo4j, Inc. — *What is a Graph Database?*  
  https://neo4j.com/docs/getting-started/graph-database/

- Neo4j, Inc. — *Cypher Manual v5*  
  https://neo4j.com/docs/cypher-manual/current/

- Robinson, I., Webber, J., Eifrem, E. — *Graph Databases*, O'Reilly Media, 2015  
  https://neo4j.com/graph-databases-book/

- DB-Engines — *MySQL vs Neo4j comparison*  
  https://db-engines.com/en/system/MySQL%3BNeo4j

- Angles, R., Gutierrez, C. — *Survey of Graph Database Models*, ACM, 2008  
  https://dl.acm.org/doi/10.1145/1322432.1322433
