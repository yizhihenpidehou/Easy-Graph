import torch
import torch.nn as nn

from easygraph.classes import Graph
from easygraph.nn import HyperGCNConv


class HyperGCN(nn.Module):
    r"""The HyperGCN model proposed in `HyperGCN: A New Method of Training Graph Convolutional Networks on Hypergraphs <https://papers.nips.cc/paper/2019/file/1efa39bcaec6f3900149160693694536-Paper.pdf>`_ paper (NeurIPS 2019).

    Parameters:
        ``in_channels`` (``int``): :math:`C_{in}` is the number of input channels.
        ``hid_channels`` (``int``): :math:`C_{hid}` is the number of hidden channels.
        ``num_classes`` (``int``): The Number of class of the classification task.
        ``use_mediator`` (``str``): Whether to use mediator to transform the hyperedges to edges in the graph. Defaults to ``False``.
        ``fast`` (``bool``): If set to ``True``, the transformed graph structure will be computed once from the input hypergraph and vertex features, and cached for future use. Defaults to ``True``.
        ``drop_rate`` (``float``, optional): Dropout ratio. Defaults to 0.5.
    """

    def __init__(
        self,
        in_channels: int,
        hid_channels: int,
        num_classes: int,
        use_mediator: bool = False,
        use_bn: bool = False,
        fast: bool = True,
        drop_rate: float = 0.5,
    ) -> None:
        super().__init__()
        self.fast = fast
        self.cached_g = None
        self.with_mediator = use_mediator
        self.layers = nn.ModuleList()
        self.layers.append(
            HyperGCNConv(
                in_channels,
                hid_channels,
                use_mediator,
                use_bn=use_bn,
                drop_rate=drop_rate,
            )
        )
        self.layers.append(
            HyperGCNConv(
                hid_channels, num_classes, use_mediator, use_bn=use_bn, is_last=True
            )
        )

    def forward(self, X: torch.Tensor, hg: "eg.Hypergraph") -> torch.Tensor:
        r"""The forward function.

        Parameters:
            ``X`` (``torch.Tensor``): Input vertex feature matrix. Size :math:`(N, C_{in})`.
            ``hg`` (``eg.Hypergraph``): The hypergraph structure that contains :math:`N` vertices.
        """
        if self.fast:
            if self.cached_g is None:
                # import time
                # start = time.time()
                self.cached_g = Graph.from_hypergraph_hypergcn(
                    hg, X, self.with_mediator
                )
                # end = time.time()
                # print("eg from_hypergraph_hypergcn:",end-start)
                # print("cached_g:",len( self.cached_g.nodes),len( self.cached_g.edges))
                # print("self.cached_g cache:",self.cached_g.cache.keys())
            for layer in self.layers:
                # import time
                # start = time.time()
                X = layer(X, hg, self.cached_g)
                # end = time.time()
                # print("eg HyperGCNConv:", end - start)
        else:
            for layer in self.layers:
                X = layer(X, hg)
        return X
