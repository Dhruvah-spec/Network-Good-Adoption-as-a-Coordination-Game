## Calculates number of rule sets that guarantee convergence to a nash equilibrium within 3 rounds
## Does not use self-inclusion logic for rule 3

import itertools
import pandas as pd
import networkx as nx

def find_converging_rules_no_self(G, filename=" "):
    nodes = sorted(list(G.nodes()))
    n = len(nodes)
    
    # 1. Generate combinations
    all_initial_states = [dict(zip(nodes, s)) for s in itertools.product([0, 1], repeat=n)]
    all_rule_combinations = list(itertools.product([1, 2, 3], repeat=n))
    
    winning_rules = []

    for r_tuple in all_rule_combinations:
        rules_dict = dict(zip(nodes, r_tuple))
        works_for_all_states = True
        
        for state_dict in all_initial_states:
            curr_state = state_dict.copy()
            converged = False
            
            # 2. Simulate 3 transitions
            for _ in range(3):
                next_state = {}
                for node in nodes:
                    rule = rules_dict[node]
                    if rule == 1:
                        next_state[node] = curr_state[node]
                    elif rule == 2:
                        nb = list(G.neighbors(node))
                        moves = [curr_state[i] for i in (nb if nb else [node])]
                        next_state[node] = 1 if sum(moves) >= len(moves) / 2 else 0
                    elif rule == 3:
                        # Logic: Neighbors of neighbors, EXCLUDING current node
                        nn = {sn for nb in G.neighbors(node) for sn in G.neighbors(nb)}
                        nn.discard(node) 
                        moves = [curr_state[i] for i in (list(nn) if nn else [node])]
                        next_state[node] = 1 if sum(moves) >= len(moves) / 2 else 0
                
                curr_state = next_state
                if sum(curr_state.values()) == n or sum(curr_state.values()) == 0:
                    converged = True
                    break
            
            if not converged:
                works_for_all_states = False
                break
        
        if works_for_all_states:
            winning_rules.append(r_tuple)

    # 3. Export to Excel
    df_winning = pd.DataFrame(winning_rules, columns=[f"Player_{i+1}" for i in range(n)])
    summary_df = pd.DataFrame({
        "Metric": ["Total Rules Checked", "Universal Convergers"],
        "Value": [len(all_rule_combinations), len(winning_rules)]
    })

    with pd.ExcelWriter(filename) as writer:
        df_winning.to_excel(writer, sheet_name='Rules', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    return len(winning_rules)

# Define Topology
G = nx.Graph()
G.add_edges_from([ ])

count = find_converging_rules_no_self(G)
print(f"Results saved. Found {count} universal rule sets.")
