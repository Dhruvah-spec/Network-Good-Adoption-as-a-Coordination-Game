## Finds the number of nash equilibria for a given network topology
## Calculates payoffs associated with all possible combinations of 'A' and 'D'

import itertools
import networkx as nx

def solve_game():
    # 1. Define the network structure
    G = nx.Graph()
    G.add_edges_from([ ])
    
    nodes = sorted(G.nodes())
    num_nodes = len(nodes)
    
    # 2. Define the payoff function
    def calculate_payoff(player, strategy_profile):
        my_choice = strategy_profile[player]
        payoff = 0
        
        for neighbor in G.neighbors(player):
            neighbor_choice = strategy_profile[neighbor]
            
            if my_choice == 'G':
                if neighbor_choice == 'G':
                    payoff += 1  # Friend plays G when I play G
                else:
                    payoff -= 1  # Friend plays N when I play G
            else: # My choice is 'N'
                if neighbor_choice == 'A':
                    payoff -= 1  # Friend plays G when I play N
                else:
                    payoff += 0  # Friend plays N when I play N
        return payoff

    # 3. Check every possible strategy combination
    strategies = ['A', 'D']
    all_profiles = list(itertools.product(strategies, repeat=num_nodes))
    nash_equilibria = []

    for profile_tuple in all_profiles:
        # Create a dictionary mapping Player ID -> Strategy
        current_profile = dict(zip(nodes, profile_tuple))
        
        is_nash = True
        for player in nodes:
            current_p = calculate_payoff(player, current_profile)
            
            # Switch strategy to see if payoff improves
            alt_choice = 'D' if current_profile[player] == 'A' else 'A'
            alt_profile = current_profile.copy()
            alt_profile[player] = alt_choice
            
            alt_p = calculate_payoff(player, alt_profile)
            
            if alt_p > current_p:
                is_nash = False
                break
        
        if is_nash:
            nash_equilibria.append(current_profile)

    # 4. Print Results
    print(f"Total Nash Equilibria found: {len(nash_equilibria)}")
    print("-" * 40)
    for i, eq in enumerate(nash_equilibria, 1):
        print(f"Equilibrium {i}:")
        payoffs = {n: calculate_payoff(n, eq) for n in nodes}
        for n in nodes:
            print(f"  Player {n}: Choice={eq[n]}, Payoff={payoffs[n]}")
        print()

if __name__ == "__main__":
    solve_game()
