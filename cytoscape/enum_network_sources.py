import os
from enum import Enum
import json

import yaml


class NetworkSource(Enum):
    GENE_MANIA = 'gene_mania'
    STRING = 'stringdb'
    INTACT = 'intact'
    GENERAL = 'all'
    def __init__(self, source_name):
        self.source_name = source_name
        self._node_keys = None
        self._edge_keys = None
        self._main_name = None
        self._desired_data = None

    def get_type_label(self):
        """
        This will just keep the way I name the property type in the network
        :return:
        """
        return "node_type"

    def get_node_keys(self):
        if self._node_keys is None:
            self._load_keys()
        return self._node_keys

    def get_edge_keys(self):
        if self._edge_keys is None:
            self._load_keys()
        return self._edge_keys

    def get_main_name(self):
        if self._main_name is None:
            self._load_keys()
        return self._main_name

    def get_desired_data(self):
        if self._desired_data is None:
            self._load_desired_data()
        return self._desired_data

    def _load_keys(self):
        cwd = os.getcwd()
        file_name = cwd.split("Muscle_wasting")[0]+"/cytoscape/Data/Apps_details.yaml"
        with open(file_name, 'r') as f:
            keys = yaml.safe_load(f)
            keys = keys[self.source_name]
        self._node_keys = keys.get('node_keys', {})
        self._edge_keys = keys.get('edge_keys', {})
        self._main_name = keys.get('main_name', {})

    def _load_desired_data(self):
        cwd = os.getcwd()
        file_name = cwd.split("Muscle_wasting")[0] + "/cytoscape/Data/properties_2_keep.yaml"
        with open(file_name, 'r') as f:
            keys = yaml.safe_load(f)
            specific = []
            general = []
            if self.source_name in keys:
                specific = keys[self.source_name]
            if self.GENERAL.source_name in keys:
                general = keys[self.GENERAL.source_name]
            specific.extend(general)
        self._desired_data = specific


