## Simulates all possible outcomes of the game for 3 rounds.
## Self-Inclusion Logic for Rule 3

import itertools
import pandas as pd
import networkx as nx

def get_copy_set_self(G, node, rule):
    """Rule 3: Self-Copy logic (Includes the node itself)."""
    if rule == 1:
        return {node}
    elif rule == 2:
        neighbors = set(G.neighbors(node))
        return neighbors if neighbors else {node}
    elif rule == 3:
        # Neighbors of neighbors + Self-Inclusion
        nn = {sn for nb in G.neighbors(node) for sn in G.neighbors(nb)}
        nn.add(node) 
        return nn
    return {node}

def get_next_state(G, current_state, rules_dict, num_players):
    next_state = {}
    for node in range(num_players):
        c_set = get_copy_set_self(G, node, rules_dict[node])
        vals = [current_state[p] for p in c_set]
        next_state[node] = 1 if sum(vals) >= len(vals) / 2 else 0
    return next_state

def run_exhaustive_simulation(edges, num_players, output_file=" "):
    G = nx.Graph()
    G.add_nodes_from(range(num_players))
    G.add_edges_from(edges)
    
    # 1. Generate all 3^6 Rule Combinations and 2^6 Initial States
    rule_combos = list(itertools.product([1, 2, 3], repeat=num_players))
    initial_states = list(itertools.product([0, 1], repeat=num_players))
    target_consensus = {'1' * num_players, '0' * num_players}
    
    all_results = []
    
    print(f"Simulating {len(rule_combos) * len(initial_states)} transitions...")

    for r_tuple in rule_combos:
        rules_dict = dict(zip(range(num_players), r_tuple))
        rule_str = "-".join(map(str, r_tuple))
        
        # Pre-calculate Copy Sets for this rule combo to save time
        copy_sets = {}
        for i in range(num_players):
            c_set = sorted([p + 1 for p in get_copy_set_self(G, i, rules_dict[i])])
            copy_sets[f"P{i+1} Copy Set"] = str(c_set)

        for s_tuple in initial_states:
            curr = dict(zip(range(num_players), s_tuple))
            path = ["".join(map(str, s_tuple))]
            
            # Simulate T1, T2, T3
            temp = curr.copy()
            for _ in range(3):
                temp = get_next_state(G, temp, rules_dict, num_players)
                path.append("".join(map(str, [temp[i] for i in range(num_players)])))
            
            t0, t1, t2, t3 = [s.zfill(num_players) for s in path]
            
            # 2. Classification Logic
            if t3 in target_consensus:
                category = "Consensus"
            elif t2 == t3:
                category = "Deadlock (Fixed Point)"
            elif t0 == t2 or t1 == t3:
                category = "Cycle (Oscillation)"
            else:
                category = "Other (Transitioning)"
            
            row = {
                "Rule Configuration": rule_str,
                "T0": t0, "T1": t1, "T2": t2, "T3": t3,
                "Classification": category
            }
            row.update(copy_sets)
            all_results.append(row)

    # 3. Export to Excel with formatting
    df = pd.DataFrame(all_results)
    t_cols = ['T0', 'T1', 'T2', 'T3']
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='All Transitions')
        ws = writer.sheets['All Transitions']
        # Set T columns to Text format to preserve leading zeros
        for col_idx, col_name in enumerate(df.columns):
            if col_name in t_cols:
                for row_idx in range(len(df) + 1):
                    ws.cell(row=row_idx+1, column=col_idx+1).number_format = '@'

    print(f"Simulation complete. Results saved to {output_file}.")

# --- EXECUTION ---
# Define your 6-player Star-Branch topology
my_edges = []
run_exhaustive_simulation(my_edges, 6)
