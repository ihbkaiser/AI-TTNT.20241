import webview
import json 
import networkx as nx

# class Api:
#     def send_coordinates(self, coords):
#         start_coords, end_coords = coords
#         print(f"Start Coordinates: {start_coords}")
#         print(f"End Coordinates: {end_coords}")
#         # Here you can add code to process the coordinates, e.g., calculate the shortest path
        
        
def load_graph(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    G = nx.Graph()
    
    for node in data['nodes']:
        G.add_node(node['id'], pos=(node['lat'], node['lng']))
    
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    return G

def shortest_path(graph, start, end):
    return nx.shortest_path(graph, source=start, target=end, weight='weight')



class Api:
    def __init__(self):
        self.graph = self.load_graph('graph_data.json')

    def load_graph(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        G = nx.Graph()
        
        for node in data['nodes']:
            G.add_node(node['id'], pos=(node['lat'], node['lng']))
        
        for edge in data['edges']:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
        
        return G

    def send_coordinates(self, coords):
        start = self.find_nearest_node(coords[0])
        end = self.find_nearest_node(coords[1])
        path = nx.shortest_path(self.graph, source=start, target=end, weight='weight')
        lst = []
        lst.append(coords[0])
        for node in path:
            lst.append(self.graph.nodes[node]['pos'])
        lst.append(coords[1])
        return lst 

    def find_nearest_node(self, coord):
        min_dist = float('inf')
        nearest_node = None
        for node, data in self.graph.nodes(data=True):
            dist = (data['pos'][0] - coord[0])**2 + (data['pos'][1] - coord[1])**2
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        return nearest_node



if __name__ == '__main__':
    api = Api()
    window = webview.create_window('WebView with Map Click', 'test.html', js_api=api)
    webview.start(debug=True, http_server=True)