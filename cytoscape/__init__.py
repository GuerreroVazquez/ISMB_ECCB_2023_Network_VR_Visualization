# import dash
# import dash_cytoscape as cyto
# from dash import html
import json

from cytoscape.enum_network_sources import NetworkSource

source = NetworkSource.GENE_MANIA

# app = dash.Dash(__name__)
  # this will vary depending on the app that I use in cytoscape

false = False
true = True


# app.layout = html.Div([

# cyto.Cytoscape(
#    id='cytoscape-two-nodes',
#    layout={'name': 'preset'},
#   style={'width': '100%', 'height': '400px'},
#   elements=elements
# )])
def read_cytoscape_json(cytoscape_file='test.cyjs'):
    """
    This function will take the json file and return the data in json format as well
    :param cytoscape_file:
    :return:  json
    """
    with open(cytoscape_file, 'r') as f:
        data = json.load(f)
        return data


def save_cytoscape_json(json_file, cytoscape_file_name='cytoscape_from_python.cyjs'):
    """
    This function takes a json file
    :param json_file:
    :param cytoscape_file_name:
    :return:
    """
    with open(cytoscape_file_name, 'w') as outfile:
        json.dump(json_file, outfile)


def get_relationships(edges, nodes):
    """
    Takes the metadata of the edges and the nodes and return a list of tuples with the
    relationship on format (protein1, protein2)
    The edges shouls alrady have the parameters source and target with the value of protein_name
    :param edges: list of json of each edge
    :param nodes: list of json of each node
    :return: list of tuples
    """

    for node in nodes:
        node['source'] = 'Cytoscape'
        node['type'] = 'protein'

    relationships = []
    for edge in edges:
        source_name = edge['source']
        target_name = edge['target']
        relationship = (source_name, target_name)
        relationships.append(relationship)

    return relationships


def get_id_name_map(nodes):
    """
    This funtion should return a dictionary of id: name of the nodes
    :param nodes:
    :return:
    """
    name_id_map={}
    unique_names={}
    for node in nodes:
        n_id = node['data']['id']
        if source.get_main_name() in node["data"]:
            n_name = node['data'][source.get_main_name()]
        else:
            print("NOOOO")
        name_id_map[n_id] = n_name
        if n_name not in unique_names:
            unique_names[n_name]=n_id

    return name_id_map, unique_names

    pass


def clean_edges(edges, name_id_map, unique_names):
    """This function should add the values target and source with
    whatever protein_name is using now"""
    for edge in edges:
        try:
            e_id = edge['data']['source']
            edge['source']= name_id_map[e_id]
            edge['data']['source'] = unique_names[edge['source']]
            e_id = edge['data']['target']
            edge['target'] = name_id_map[e_id]
            edge['data']['target'] = unique_names[edge['target']]

        except Exception as e:
            print(e)
    return edges


def format_cytoscape_json(cytoscape_json):
    """
    This function takes the Json file and takes the edges and nodes separately
    and format in a way that I can feed to the networkX graph.

    :return: the list of dictionaries of the nodes, the list of dictionaries of the edges (metadata n stuff)
    and the list of tuples with the relationships
    """
    cytoscape = cytoscape_json
    c_elements = cytoscape["elements"]
    nodes = c_elements["nodes"]
    edges = c_elements["edges"]
    name_id_map, unique_names = get_id_name_map(nodes)
    edges = clean_edges(edges, name_id_map, unique_names)
    relationships = get_relationships(edges, nodes)
    return nodes, edges, relationships


def create_cytoscape_node(node_name, node_data={}, node_position={}, source='python_cut', node_type='unspecified',
                          selected=False):
    """
    This node will return a dictionary corresponding to the node as cytoscape process them
    :param node_name: str
    :param node_data: dict
    :param node_position: dict
    :param source: Where is the node comming from
    :param node_type: What type of biological element is it
    :param selected: If the node is selected
    :return:
    """
    node = {'data': node_data, 'position': node_position, 'id': node_name, 'source': source, 'type': node_type,
            'selected': selected}
    return node

def create_cytoscape_edge(source, target, node_data={}, node_position={},
                          selected=False, weight=1):
    """
    This node will return a dictionary corresponding to the node as cytoscape process them
    :param weight:
    :param node_data: dict
    :param node_position: dict
    :param source: Where is the node coming from
    :param selected: If the node is selected
    :return:
    """
    node = {'data': node_data, 'position': node_position, 'source': source, 'target': target,
            'selected': selected, 'weight':weight}
    return node


if __name__ == '__main__':
    # app.run_server(debug=True)
    pass
