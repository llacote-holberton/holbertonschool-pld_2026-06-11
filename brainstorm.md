
**NEO4J**



# **Phase de recherches**

**        → QUE STOCK-IL?**

                -> **NOEUD** : ça correspond à par exemple une personne, un film, une ville peut importe  (ALICE)

                -> **PROPRIÉTÉS** : les informations liées aux noeuds (Nom: ALICE -> 28 ans / Ville : PARIS )

                -> **RELATIONS** : Une entre 2 noeuds ( ALICE soeur de BOB, ALICE et BOB sont 2 noeuds différents ) 



**        → Comment range-t-il les données?**

                -> Les données d’un **noeud **sont organisées par catégorie appelé **labels** (ex: :Person, :Product) pour catégoriser / typer les noeuds

                -> Les **relations **sont toujours orientées (un sens de départ et d’arrivée). Chaque relation possède un type unique (ex: ACHETE, CONNAIT, HABITE\_A)

                

        **Spécificité :**

**                -> Index-free adjacency : **Chaque noeud content directement, en mémoire, des pointeurs physiques (sous forme de liste chainée)

               * **                                        **Ça signifie qu’il n’y a aucune jointure par rapport à Mysql par exemple
**                -> fichiers de stockage séparés :   **1 fichier pour les noeuds 

   * **                                                                     **1 fichier pour les relations 
**                                                                           **1 fichier pour les propriétés 

**                                                                           **1 fichier pour les labels / types

**        -> Pourquoi existe-t-il?**

**                ->**Pour pouvoir créer des applications robustes à la charge dont le fonctionnement repose avant tout sur les relations entre les données. 

                    Par exemple un réseau social (données clé : qui connaît qui, qui travaille avec qui) ou un système de recommandations de contenu associé à un site de streaming.





----------------------------------------------------



# Traitement des questions

### 1. C'est quoi ce modèle, et pourquoi existe-t-il ? 



Neo4j c'est une base de données qui stocke des connexions entre des choses.

Imagine Netflix — tu as des utilisateurs, des films, des genres. 

La question intéressante c'est pas "liste-moi tous les films", c'est "Alice a regardé Inception, Bob aussi, ils se suivent, et un nouveau film Sci-Fi sort — qui notifier ?"

Dans une base classique comme MySQL, répondre à cette question c'est des jointures dans tous les sens, c'est lent et compliqué.



### 2. Comment les données sont elles représentées ? 



Il y a 4 opérations de base. On **crée** des nœuds et des relations pour alimenter le graphe. On **lit** des données en décrivant le chemin qu'on veut trouver — par exemple "trouve-moi tous les utilisateurs qui ont regardé un film Sci-Fi". On **modifie** les propriétés d'un nœud ou d'une relation quand une information change. Et on **supprime** un nœud en supprimant automatiquement toutes ses relations en même temps.



La grande différence avec SQL c'est que pour lire ou modifier des données, on décrit un dessin — Alice suit Bob qui a regardé Inception — et Neo4j trouve tout ce qui ressemble à ce dessin dans la base.



SCHEMA DE REPRESENTATION DES DONNEES A REPRENDRE DE SOUFIANE



### 3. Comment fonctionnent les opérations de base

CRUD -> 

**C**: Cypher propose deux méthodes : CREATE classique qui va créer quoiqu'il arrive quitte à créer un doublon.

    et MERGE qyi est l'équivalent de "Retourne l'entrée si elle existe (MATCH) sinon créée la (CREATE).

    Même syntaxe que l'on créée un Node ou un Relationship

    Noter cependant qu'il faut être rigoureux sur la syntaxe :  MERGE (a:Utilisateur {nom: "Alice"})-[:A\_AIMÉ]->(m:Film {titre: "Matrix"}) crééerait une nouvelle Alice si une entité Alice existe mais qu'elle n'a pas aimé Matrix.

    Il vaut mieux dans ce cas d'abord s'assurer de l'existence des noeuds, puis faire une requête séparée pour la relation en elle-même.

**R**: Cypher utilise le mot-clé MATCH comme "équivalent" au SELECT d'une base relationnelle. Il faut forcément l'associer à un RETURN (équivalent d'un .query(xxx) -> .fetchall/fetchone pour un ORM : d'abord on demande à générer un ensemble de résultats, ensuite on en récupère tout ou partie.

U: Il faut utiliser un MATCH pour "sélectionner les entités à mettre à jour" puis une ou plusieurs commandes SET pour (re)définir les propriétés.

D: Comme le modèle Graph distingue les entités de leur "propriétés" on a deux commandes distinctes : REMOVE permet de supprimer UNE propriété parmi celles d'une entité. Tandis que DELETE supprimer l'entité entièrement mais uniquement lorsque celle-ci n'a plus aucune relation.





### 4. Quels sont les cas d'usage ? 

Tous les services ou tous les types de traitements de données qui s'appuient sur les relations, que ce soit une combinaison de contraintes de relations (ex je veux les utilisateurs d'un site de streaming qui aiment les Romances et suivent tel directeur  et aiment tels acteurs) ou une grande chaîne de relations (trouve moi tous les gens que connaît X que connaît Y qui est le petit frère du cousin par alliance du père de Tom Cruise).



### 5. Quels compromis ou limites?

Neo4j excelle pour suivre des relations (chemins, recommandations, fraude) quel que soit le nombre de sauts, contrairement au SQL qui ralentit avec les jointures multiples. En revanche, il est moins efficace pour les gros calculs globaux (agrégations sur des millions de lignes), domaine où le relationnel ou les bases colonnes sont meilleurs. Ses performances dépendent fortement de la mémoire disponible. Enfin, son écosystème (outils, formation) est moins mature que celui de SQL.



### 6. Comment se compare-t-il au relationnel?

En relationnel, les données sont rangées dans des tables séparées, et les liens entre elles (comme "Alice a acheté Livre X") doivent être recalculés à chaque requête grâce à des jointures (JOIN). En graphe (Neo4j), ce lien est stocké directement, une fois pour toutes, comme un pointeur entre les deux éléments. Résultat : suivre des relations est beaucoup plus rapide en graphe, surtout si on enchaîne plusieurs liens. Mais pour des opérations simples sur de gros tableaux de données (filtrer, compter, faire des totaux), le relationnel reste souvent plus efficace. En résumé : le relationnel est fait pour des données en tableaux, le graphe pour des données en réseau.

## 

### **7. Comment pourrions-nous l'utiliser dans un contexte de modélisation polyglotte de persistence de données?**

Rappel : on entend par "persistence polyglotte" l'usage combiné de différents paradigmes de modélisation de données, afin de profiter des points forts de chacun tout en réduisant leurs contraintes / limites.

Ce qui implique évidemment une infrastructure conséquente et une architecture logicielle complexe, réservant donc ça aux cas d'usages les plus complexes ou les plus gourmands. 

Typiquement des plates-formes type Youtube, Google Maps, Netflix ou Linkedin pourraient en avoir l'usage.



Exemple de Youtube

Youtube est une plate-forme de streaming avec des contraintes complémentaires issues de différents points de vue : gestion de contenu pur avec statistiques agrégées (combien de contenu, durée moyenne, nombre moyen de visites etc), promotion dynamique de contenu (calculer le "potentiel d'intérêt" d'une vidéo pour un utilisateur selon l'historique et les souscriptions ), diffusion de contenu riche (flux brut, métadonnées, sous-titres, commentaires etc).

Si l'on met de côté la sur-complexité et la redondance due à une organisation "multi-modèle" on pourrait dire...

1/ Base SQL classique pour la gestion de contenu (grande performance pour les requêtes "verticales" du genre "nombre de contenu, durée moyenne, catégories").

2/ Graph pour la gestion des recommendations (base dans laquelle seule les informations pertinentes d'une vidéo pour la recommendation sont stockées : titre, genre, réalisateur, acteur principal. Idem pour les utilisateurs : identifiant et éventuellement pays ?).

3/ Document pour la diffusion (un élément de la base porte TOUTES les informations liées à la vidéo, mis à part les commentaires)..





