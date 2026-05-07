## Calculates the number of rule sets that guarantee convergence to a nash equilibrium within three rounds
## Uses Self-Inclusion Logic for Rule 3

import itertools
import pandas as pd
import networkx as nx

def get_next_state_universal(G, current_state, rules):
    """
    Calculates the next state based on self-inclusion logic.
    """
    next_state = {}
    nodes = sorted(list(G.nodes()))
    
    for node in nodes:
        rule = rules[node]
        
        if rule == 1: # Rule I: Play whatever move I played again
            next_state[node] = current_state[node]
            
        elif rule == 2: # Rule II: Neighbor Majority
            neighbors = list(G.neighbors(node))
            if not neighbors:
                next_state[node] = current_state[node]
            else:
                moves = [current_state[n] for n in neighbors]
                next_state[node] = 1 if sum(moves) >= len(moves) / 2 else 0
                
        elif rule == 3: # Rule III: Neighbors' Neighbors (Self-Inclusion)
            # Find neighbors of neighbors; includes self if a path exists (e.g., A-B-A)
            nn = {sn for n in G.neighbors(node) for sn in G.neighbors(n)}
            if not nn:
                next_state[node] = current_state[node]
            else:
                moves = [current_state[n] for n in nn]
                next_state[node] = 1 if sum(moves) >= len(moves) / 2 else 0
                
    return next_state

def find_always_converging_rules(G, filename=" "):
    nodes = sorted(list(G.nodes()))
    n = len(nodes)
    
    # Generate all possible initial states (2^n)
    all_initial_states = [dict(zip(nodes, s)) for s in itertools.product([0, 1], repeat=n)]
    # Generate all rule combinations (3^n)
    all_rule_combinations = list(itertools.product([1, 2, 3], repeat=n))
    
    winning_rules = []

    for r_tuple in all_rule_combinations:
        rules_dict = dict(zip(nodes, r_tuple))
        works_for_all_states = True
        
        for state_dict in all_initial_states:
            curr_state = state_dict.copy()
            converged = False
            
            # Check convergence in exactly 3 transitions
            for _ in range(3):
                curr_state = get_next_state_universal(G, curr_state, rules_dict)
                total_sum = sum(curr_state.values())
                if total_sum == n or total_sum == 0:
                    converged = True
                    break
            
            if not converged:
                works_for_all_states = False
                break
        
        if works_for_all_states:
            winning_rules.append(r_tuple)

    # Export to Excel
    df_winning = pd.DataFrame(winning_rules, columns=[f"Player_{i+1}" for i in range(n)])
    summary_data = {
        "Metric": ["Total Rules Checked", "Universal Convergers Found"],
        "Value": [len(all_rule_combinations), len(winning_rules)]
    }
    df_summary = pd.DataFrame(summary_data)

    with pd.ExcelWriter(filename) as writer:
        df_winning.to_excel(writer, sheet_name='Converging Rules', index=False)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
    
    return len(winning_rules)

# --- Define Topology ---
# Change this to any graph: nx.cycle_graph(6), nx.complete_graph(6), etc.
G = nx.Graph() 
G.add_edges_from([])

count = find_always_converging_rules(G)
print(f"Search complete. Found {count} universal rule sets. Results saved to Excel.")
