import json
import os

import torch

from easygraph.convert import dict_to_hypergraph

from .eg_dataset import EasyGraphDataset
from .hypergraph.load_dataset import request_json_from_url
from .utils import _get_eg_url
from .utils import tensor


class Email_Enron(EasyGraphDataset):
    _urls = {
        "email-enron": (
            "easygraph-data-email-enron/-/raw/main/email-enron.json?inline=false"
        ),
        "email-eu": "easygraph-data-email-eu/-/raw/main/email-eu.json?inline=false",
    }

    def __init__(
        self,
        raw_dir=None,
        force_reload=False,
        verbose=True,
        transform=None,
        save_dir="./",
    ):
        name = "email-enron"
        self.url = _get_eg_url(self._urls[name])
        super(Email_Enron, self).__init__(
            name=name,
            url=self.url,
            raw_dir=raw_dir,
            force_reload=force_reload,
            verbose=verbose,
            transform=transform,
            save_dir=save_dir,
        )

    @property
    def url(self):
        return self._url

    @property
    def save_name(self):
        return self.name

    def __getitem__(self, idx):
        assert idx == 0, "This dataset has only one graph"
        if self._transform is None:
            return self._g
        else:
            return self._transform(self._g)

    def load(self):
        graph_path = os.path.join(self.save_path, self.save_name + ".json")
        with open(graph_path, "r") as f:
            self.load_data = json.load(f)

    def has_cache(self):
        graph_path = os.path.join(self.save_path, self.save_name + ".json")
        if os.path.exists(graph_path):
            return True
        return False

    def download(self):
        print("download...")
        if self.has_cache():
            self.load()
        else:
            root = self.raw_dir
            data = request_json_from_url(self.url)
            with open(os.path.join(root, self.save_name + ".json"), "w") as f:
                json.dump(data, f)
            self.load_data = data

    def process(self):
        """Loads input data from data directory and transfer to target graph for better analysis
        """

        self._g, edge_feature_list = dict_to_hypergraph(self.load_data, is_dynamic=True)

        self._g.ndata["hyperedge_feature"] = tensor(
            range(1, len(edge_feature_list) + 1)
        )

        # self._g.ndata["incidence_matrix"] = self._g.incidence_matrix

    @url.setter
    def url(self, value):
        self._url = value
