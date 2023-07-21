from easygraph.datasets.get_sample_graph import *

from .email_enron import Email_Enron
from .hypergraph import *


try:
    from easygraph.datasets.gnn_benchmark import *
    from easygraph.datasets.karate import KarateClubDataset

    from .citation_graph import CitationGraphDataset
    from .citation_graph import CiteseerGraphDataset
    from .citation_graph import CoraBinary
    from .citation_graph import CoraGraphDataset
    from .citation_graph import PubmedGraphDataset
    from .cooking_200 import Cooking200
    from .ppi import LegacyPPIDataset
    from .ppi import PPIDataset

except:
    print(
        " Please install Pytorch before use dataset such as"
        " KarateClubDataset、CitationDataset、PPIDataset、LegacyPPIDataset"
    )
