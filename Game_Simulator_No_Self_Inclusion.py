## Simulates all possible outcomes  of the game (for every possible starting state and rule configuration) 3 rounds
## No Self-Inclusion for Rule 3
## Gives the copy sets for each player
## Classfies each outcome as 'deadlock', 'oscillating', or 'concensus' based on how states change from round to round

import itertools
import pandas as pd
import networkx as nx

def get_copy_set(G, node, rule, self_copy=False):
    """
    Returns the set of nodes a player watches.
    Rule 3: No Self-Copy logic (Excludes the node itself).
    """
    if rule == 1:
        return {node}
    elif rule == 2:
        neighbors = set(G.neighbors(node))
        return neighbors if neighbors else {node}
    elif rule == 3:
        # Neighbors of neighbors
        nn = {sn for nb in G.neighbors(node) for sn in G.neighbors(nb)}
        if not self_copy and node in nn:
            nn.remove(node) # Explicitly remove self
        return nn if nn else {node}
    return {node}

def get_next_state(G, current_state, rules_dict):
    next_state = {}
    nodes = sorted(list(G.nodes()))
    for node in nodes:
        c_set = get_copy_set(G, node, rules_dict[node], self_copy=False)
        vals = [current_state[p] for p in c_set]
        # Majority rule: 1 if sum >= half of set size
        next_state[node] = 1 if sum(vals) >= len(vals) / 2 else 0
    return next_state

def run_full_simulation(edges, num_players, output_file=" "):
    G = nx.Graph()
    G.add_nodes_from(range(num_players))
    G.add_edges_from(edges)
    
    nodes = range(num_players)
    initial_states = list(itertools.product([0, 1], repeat=num_players))
    rule_combinations = list(itertools.product([1, 2, 3], repeat=num_players))
    
    all_transitions = []
    stats = {"Deadlock": 0, "Cycle": 0, "Other": 0, "Consensus": 0}
    target_states = {"0"*num_players, "1"*num_players}

    # 1. Simulate every rule set against every state
    for r_tuple in rule_combinations:
        rules_dict = dict(zip(nodes, r_tuple))
        rule_str = "-".join(map(str, r_tuple))
        
        for s_tuple in initial_states:
            curr = dict(zip(nodes, s_tuple))
            path = ["".join(map(str, s_tuple))]
            
            # 3 Transitions (T0 to T3)
            temp = curr.copy()
            for _ in range(3):
                temp = get_next_state(G, temp, rules_dict)
                path.append("".join(map(str, [temp[i] for i in nodes])))
            
            t0, t1, t2, t3 = path
            
            # Classification
            if t3 in target_states:
                category = "Consensus"
            elif t2 == t3:
                category = "Deadlock"
            elif t0 == t2 or t1 == t3:
                category = "Cycle"
            else:
                category = "Other"
            
            stats[category] += 1
            all_transitions.append({
                "Rule Set": rule_str,
                "Path": f"T0:{t0}, T1:{t1}, T2:{t2}, T3:{t3}",
                "Classification": category
            })

    # 2. Generate Copy Sets for all rule combinations
    copy_set_data = []
    for r_tuple in rule_combinations:
        row = {"Rule Combination": "-".join(map(str, r_tuple))}
        for i in range(num_players):
            c_set = sorted([p+1 for p in get_copy_set(G, i, r_tuple[i], self_copy=False)])
            row[f"P{i+1} Copy Set"] = str(c_set)
        copy_set_data.append(row)

    # 3. Save to Excel
    with pd.ExcelWriter(output_file) as writer:
        pd.DataFrame(all_transitions).to_excel(writer, sheet_name='Transitions', index=False)
        pd.DataFrame(copy_set_data).to_excel(writer, sheet_name='Copy Sets', index=False)
        pd.DataFrame([stats]).to_excel(writer, sheet_name='Summary Statistics', index=False)

    print(f"Simulation Complete. Results saved to {output_file}")
    print("Summary:", stats)

# --- EXECUTION ---
# Example Topology (Star-Branch)
my_edges = []
run_full_simulation(my_edges, 6)
