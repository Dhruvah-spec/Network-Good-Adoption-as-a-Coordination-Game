# Network-Good-Adoption-as-a-Coordination-Game 🎮

Coordination games involve decision-making scenarios in which two or more players are required to choose between options with payoffs dependent on the others’ actions and where the highest level of utility is achieved by converging on a common set of strategies. Games like ‘Battle of Sexes’ and 'Stag Hunt' serve as a classic archetypes for representing these kinds of situations. 

This project aims to model the problem of individuals deciding whether to adopt a network good as a coordination game. These situations require individuals to align their decisions with those of other people, while other people are simultaneously trying to do the same thing. The role played by network topology in facilitating coordination is explored

## Structure
This study treats the problem of individuals making adoption decisions as a 6 player round-based coordination game taking place within a network structure. Nodes in the network represent individuals and links represent friendships. For every round each player chooses between two strategies- Adopt (A) and Don’t Adopt (D) with payoffs given by the following table:

| Player $i$ Strategy | Friend $j$ plays **Adopt(A)** | Friend $j$ plays **Don't Adopt (D)** |
| :--- | :---: | :---: |
| **Adopt (A)** | `+1` | `-1` |
| **Don't Adopt (D)** | `-1` | `0` |

The rows represent the player, and the columns represent all the players to which this player is connected, ie the player’s friends. If the player chooses A, a unit of 1 is received for every friend that also chooses A, but it loses a unit of 1 for every one of its friends that don’t choose A. If the player chooses D, it loses a unit of 1 for every friend that chooses to play and gets a payoff of 0 for every friend that also chooses D. In this scenario, common knowledge of rationality and complete information would result in everyone choosing to play A as it is collectively known that this yields the highest benefit for all. To explore more interesting dynamics, this study relaxes the assumption of common knowledge of rationality and instead supposes that players have different beliefs about how their friends take decisions and use heuristic rules based on those beliefs to make their own decisions. It is also assumed that they are aware of the network structure.

## Rule Archetypes
| Type            | Decision Rule                                                                 | Belief                                                                                          |
|-----------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Fixed (I)          | Plays the same move in every round.                                          | Friends will copy them, so they do not need to copy others.                                      |
| Adaptive (II)       | Copies the move played by the majority of friends in the previous round (plays A if no clear majority). | Friends only copy themselves, so they must copy friends to achieve coordination.                |
| Forward Looking (III) | Copies the move played by the majority of friends’ friends in the previous round (plays A if no clear majority). | Friends make decisions by copying their own friends, so they must anticipate this to coordinate. |

### Variants for Rule 3:
Variant 1 - For the first variation, under rule 3, the players themselves are part of their set of friends’ friends. For example, if player 1 is friends with player 2, and if player 2 is friends with player 4, when player 1 plays rule 3, ie when he copies his friends’ friends, he will be copying the majority move out of player 1 (his own move) and player 4. This is a natural interpretation of the rule as player 1 is also player 2’s friend (because we are considering undirected networks) and so he would include himself under the set of friends’ friends. This is the self-inclusion logic for rule 3. 

Variant 2 - Under the second variation, the players playing the rule will not include their own vote in deciding what their next move should be, player 1 would be excluded from the set. Self-inclusion logic for rule 3 is not followed under this variation.

## Network Topologies
| Topology            | Description                                                                 | Key Properties                                                                                  | ASCII Diagram |
|---------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|---------------|
| Complete Graph      | Every node is connected to every other node.                                | Maximum connectivity; shortest paths; very dense (O(n²) edges).                                 | ```  A-----B  |\   /|  | \ / |  |  X  |  | / \ |  |/   \|  C-----D ``` |
| Small-World Graph   | Mostly local connections with a few long-range random links.                | High clustering + short average path lengths.                                                    | ``` A--B--C  |  |  |  D--E--F  \     /   G-----H ``` |
| Star Graph          | One central node connected to all others; no peripheral connections.        | Highly centralized; hub is critical point of failure.                                            | ```    B     |    |  C--A--D     |     E ``` |
| Spoke and Hub Graph | Multiple hubs or layered hub-spoke structure.                               | Semi-centralized; more robust than a single star.                                                | ```   B     F    |    |    C--A----E     |     D     G ``` |
