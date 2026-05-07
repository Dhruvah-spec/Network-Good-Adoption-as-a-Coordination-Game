# Network-Good-Adoption-as-a-Coordination-Game

Coordination games involve decision-making scenarios in which two or more players are required to choose between options with payoffs dependent on the others’ actions and where the highest level of utility is achieved by converging on a common set of strategies. Games like ‘Battle of Sexes’ and 'Stag Hunt' serve as a classic archetypes for representing these kinds of situations. 

This project aims to model the problem of individuals deciding whether to adopt a network good as a coordination game. These situations require individuals to align their decisions with those of other people, while other people are simultaneously trying to do the same thing. The role played by network topology in facilitating coordination is explored

## Structure
This study treats the problem of individuals making adoption decisions as a round-based coordination game taking place within a network structure. Nodes in the network represent individuals and links represent friendships. For every round each player chooses between two strategies- Adopt (A) and Don’t Adopt (D) with payoffs given by the following table:

| Player $i$ Strategy | Friend $j$ plays **Adopt(A)** | Friend $j$ plays **Don't Adopt (D)** |
| :--- | :---: | :---: |
| **Adopt (A)** | `+1` | `-1` |
| **Don't Adopt (D)** | `-1` | `0` |

The rows represent the player, and the columns represent all the players to which this player is connected, ie the player’s friends. If the player chooses A, a unit of 1 is received for every friend that also chooses A, but it loses a unit of 1 for every one of its friends that don’t choose A. If the player chooses D, it doesn’t receive or lose any units no matter what its friends do. This payoff structure was chosen to place expectations at the core of the decision problem. Whether a player chooses to adopt the good or not completely depends on what they believe their friends will do. In this scenario, common knowledge of rationality and complete information would result in everyone choosing to play A as it is collectively known that this yields the highest benefit for all. To explore more interesting dynamics, this study relaxes the assumption of common knowledge of rationality and instead supposes that players have different beliefs about how their friends take decisions and use heuristic rules based on those beliefs to make their own decisions. It is also assumed that they are aware of the network structure.
