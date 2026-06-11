# Le modèle Graph - brève présentation à travers Neo4j : principes, forces et faiblesses, cas d'usage

Le modèle de données orienté graphe se distingue des bases de données traditionnelles en plaçant les relations au même niveau d'importance que les données elles-mêmes. Neo4j est le leader mondial des systèmes de gestion de bases de données (SGBD) orientés graphes natifs.

## 1. Structure et stockage des données (Le modèle de propriétés)

Le modèle utilisé par Neo4j est appelé **Graphe de propriétés orienté et étiqueté**. Il repose sur quatre éléments fondamentaux :

### Les Nœuds (Nodes)

Représentent les entités ou objets du monde réel (ex : une personne Alice, un film Matrix, une ville Paris).

### Les Labels

Catégorisent et typent les nœuds (ex : `:Utilisateur`, `:Film`). Un nœud peut posséder plusieurs labels.

### Les Relations (Relationships)

Connectent obligatoirement deux nœuds. Elles sont toujours orientées (un sens de départ et d'arrivée) et possèdent un type unique en majuscules (ex : `[:A_AIMÉ]`, `[:HABITE_À]`).

### Les Propriétés (Properties)

Paires clé-valeur stockées directement sur les nœuds ou sur les relations pour ajouter des informations (ex : `nom: "Alice"`, `note: 5`).

### Spécificités architecturales de Neo4j

Contrairement aux SGBD relationnels qui simulent les liens à l'aide de clés étrangères et d'index, Neo4j utilise l'**Index-free Adjacency** (Adjacence sans index). Chaque nœud contient en mémoire des pointeurs physiques directs (sous forme de listes doublement chaînées) vers ses nœuds voisins. Traverser une relation se fait ainsi en temps constant **O(1)**, indépendamment de la taille globale de la base de données.

Pour optimiser ces accès, Neo4j fragmente son stockage en fichiers séparés sur le disque (un fichier pour les nœuds, un pour les relations, un pour les propriétés et un pour les labels/types).

## 2. Opérations fondamentales (CRUD avec le langage Cypher)

Cypher est le langage de requête déclaratif de Neo4j. Sa syntaxe est visuelle et utilise l'art ASCII pour représenter le graphe :

```text
(nœud)-[relation]->(nœud)
```

### Create (Création)

- `CREATE` ajoute systématiquement de nouveaux éléments, au risque de créer des doublons.
- `MERGE` agit comme un « rechercher ou créer ».

**Piège syntaxique :**

```cypher
MERGE (a:Utilisateur {nom: "Alice"})-[:A_AIMÉ]->(m:Film {titre: "Matrix"})
```

Cette requête recréera une nouvelle Alice si la relation exacte n'existe pas encore.

**Bonne pratique :**

- Effectuer d'abord un `MERGE` ou un `MATCH` sur les nœuds indépendamment.
- Puis effectuer un `MERGE` sur la relation.

### Read (Lecture)

Utilise le mot-clé `MATCH` pour décrire le motif (le « dessin ») recherché, obligatoirement associé à `RETURN` pour extraire les données (équivalent du `SELECT ... FROM` en SQL).

### Update (Mise à jour)

S'effectue en ciblant l'entité avec `MATCH`, puis en appliquant la commande `SET` pour modifier ou ajouter des propriétés.

### Delete (Suppression)

Neo4j distingue la donnée de sa structure :

- `REMOVE` supprime une propriété ou un label d'une entité.
- `DELETE` supprime définitivement un nœud ou une relation.

**Note correctrice :**

Neo4j interdit la suppression d'un nœud s'il possède encore des relations (pour éviter les relations orphelines). Il faut utiliser `DETACH DELETE` pour supprimer un nœud et toutes ses relations associées en une seule opération.

## 3. Cas d'usage, forces et limites

### Cas d'usage principaux

Neo4j excelle dès lors que la valeur de l'application repose sur l'interconnexion des données :

- **Moteurs de recommandation en temps réel**  
  (ex : recommander un film en fonction des goûts des amis et de l'historique de visionnage).

- **Détection de la fraude**  
  (ex : identifier des réseaux de comptes bancaires interconnectés par des numéros de téléphone ou des adresses IP identiques).

- **Réseaux sociaux et graphes de connaissances**  
  (gestion des structures « qui connaît qui », hiérarchies complexes).

### Compromis et limites

| Forces de Neo4j / Modèle Graphe | Limites / Compromis |
|----------------------------------|---------------------|
| Performance constante lors des sauts multiples (traversées de relations en profondeur). | Moins performant pour les calculs globaux et les agrégations de masse (ex : calculer la moyenne d'âge sur 50 millions de lignes). |
| Schéma flexible (NoSQL) : possibilité d'ajouter des propriétés ou relations sans bloquer la base. | Forte dépendance à la RAM : pour garantir l'Index-free Adjacency, le graphe doit idéalement être chargé en mémoire vive. |
| Requêtes complexes très courtes à écrire par rapport à des dizaines de `JOIN` en SQL. | Écosystème et vivier de talents moins matures que l'écosystème SQL traditionnel. |

### Exemples d'usages concrets
- UBS (banque suisse) l'utilise pour la traçabilité des données et la conformité réglementaire des échanges.
- Ebay l'utilise pour optimiser les plannings et itinéraires de livraison pour sa flotte de livreurs attitrés.
- Transport For London l'utilise pour surveiller en temps réel la charge de son réseau et identifier voire anticiper les congestions.
- BencnSci l'utilise pour faciliter la recherche de documents scientifiques basée sur de la proximité sémantique ou associative (domaine de recherche connexe, résultats expérimentaux associés à une thèse, etc).

## 4. Intégration dans une Architecture de Persistance Polyglotte

La persistance polyglotte consiste à utiliser plusieurs types de bases de données au sein d'une même architecture logicielle afin d'attribuer à chaque tâche l'outil le plus performant.

Bien qu'elle apporte une complexité technique et des risques de redondance, elle est indispensable pour les plateformes à très haute échelle (Netflix, YouTube, LinkedIn).

### Exemple d'application concret : YouTube

Pour orchestrer une plateforme comme YouTube, les responsabilités peuvent être réparties ainsi :

#### Le modèle Relationnel (SQL)

Idéal pour :

- la gestion transactionnelle ;
- la comptabilité ;
- les données structurées des créateurs ;
- les statistiques verticales strictes.

Exemples :

- requêtes de reporting ;
- nombre total de vidéos par catégorie ;
- durée moyenne des vidéos.

#### Le modèle Graphe (Neo4j)

Dédié exclusivement au moteur de recommandation.

On y stocke uniquement les métadonnées légères et connectées :

- ID de l'utilisateur ;
- ID de la vidéo ;
- genres ;
- réalisateurs ;
- abonnements.

Neo4j calcule instantanément les suggestions personnalisées en analysant les chemins de navigation des utilisateurs.

#### Le modèle Document (NoSQL – ex : MongoDB)

Utilisé pour la diffusion rapide du contenu.

Un document englobe l'ensemble des données riches d'une vidéo :

- titre ;
- description enrichie ;
- tags ;
- flux bruts ;
- sous-titres.

Cette approche permet un affichage instantané de la page sans aucune jointure.
