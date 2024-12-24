import argparse
from app import main

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run graph algorithm visualization.')
    parser.add_argument('--mode', type=str, default='dijkstra', choices=['dijkstra', 'a_star', 'bellman_ford', 'floyd_warshall'],
                        help='Algorithm mode to run (default: dijkstra)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    main()
    
