import pytest

import Constants
import cytoscape as ct
from cytoscape.enum_network_sources import NetworkSource

cytoscape_small_data_nodes = Constants.cytoscape_small_data_nodes
cytoscape_small_data_edges = Constants.cytoscape_small_data_edges


def test_read_json():
    """
    This is a simple test to check if the lecture of the Cytoscape in in the right format
    :return:
    """
    js = ct.read_cytoscape_json(cytoscape_file='test.cyjs')
    assert js['elements'] == {'nodes': cytoscape_small_data_nodes,
                              'edges': cytoscape_small_data_edges}, f"The json file is in an unexpected format."


def test_save_cytoscape_json():
    js = Constants.cytoscape_small_string_json
    ct.save_cytoscape_json(js, 'test_cytoscape.cyjs')
    js2 = ct.read_cytoscape_json('test_cytoscape.cyjs')
    assert js == js2, f"The json was saved with modifications"


def test_format_cytoscape_json():
    cytoscape = Constants.cytoscape_small_string_json
    nodes, edges, relationsips = ct.format_cytoscape_json(cytoscape)
    assert len(edges) == len(
        relationsips), f"Given that the variable 'edges' is the metadata for the relationships, this must be the " \
                       f"exact same length "
    assert nodes == Constants.cytoscape_small_data_nodes
    assert edges == Constants.cytoscape_small_data_edges
    assert relationsips == Constants.cytoscape_small_relationships



def test_enum_network_source():
    source = NetworkSource.GENE_MANIA
    x = source.get_main_name()
    assert source.get_main_name() == "gene_name"
    assert "query_term" in source.get_node_keys()
    assert "shared_name" in source.get_edge_keys()