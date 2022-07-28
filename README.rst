EasyGraph
==================

Copyright (C) <2020-2022> by Mobile Systems and Networking Group, Fudan University

.. image:: https://img.shields.io/pypi/v/Python-EasyGraph.svg
  :target: https://pypi.org/project/Python-EasyGraph/

.. image:: https://img.shields.io/pypi/pyversions/Python-EasyGraph.svg
   :target: https://pypi.org/project/Python-EasyGraph/

.. image:: https://img.shields.io/pypi/l/Python-EasyGraph
   :target: https://github.com/easy-graph/Easy-Graph/blob/master/LICENSE

- **Documentation:** https://easy-graph.github.io/
- **Source Code:** https://github.com/easy-graph/Easy-Graph
- **Issue Tracker:** https://github.com/easy-graph/Easy-Graph/issues
- **PyPI Homepage:** https://pypi.org/project/Python-EasyGraph/
- **Youtube channel:** https://www.youtube.com/channel/UCZGhOPPx8aeL30uEdpk23Aw

Introduction
------------
EasyGraph is an open source graph processing library. It is mainly written in Python and supports analysis for undirected graphs and directed graphs. EasyGraph supports various formats of graph data and covers a series of important graph mining algorithms for community detection, structural hole spanner detection, graph embedding and motif detection. Moreover, EasyGraph implements some key elements using C++ and introduces multiprocessing optimization to achieve a better efficiency.

Install
-------
Installation with ``pip``
::

    $ pip install Python-EasyGraph

or ``conda``
::

    $ conda install Python-EasyGraph

Simple Example
--------------


This example shows the general usage of methods in EasyGraph.

.. code:: python

  >>> import easygraph as eg
  >>> G = eg.Graph()
  >>> G.add_edges([(1,2), (2,3), (1,3), (3,4), (4,5), (3,5), (5,6)])
  >>> eg.pagerank(G)
  {1: 0.14272233049003707, 2: 0.14272233049003694, 3: 0.2685427766200994, 4: 0.14336430577918527, 5: 0.21634929087322705, 6: 0.0862989657474143}

This is a simple example for the detection of `structural hole spanners <https://en.wikipedia.org/wiki/Structural_holes>`_
using the `HIS <https://keg.cs.tsinghua.edu.cn/jietang/publications/WWW13-Lou&Tang-Structural-Hole-Information-Diffusion.pdf>`_ algorithm.

.. code:: python

  >>> import easygraph as eg
  >>> G = eg.Graph()
  >>> G.add_edges([(1,2), (2,3), (1,3), (3,4), (4,5), (3,5), (5,6)])
  >>> _, _, H = eg.get_structural_holes_HIS(G, C=[frozenset([1,2,3]), frozenset([4,5,6])])
  >>> H # The structural hole score of each node. Note that node `4` is regarded as the most possible structural hole spanner.
  {1: {0: 0.703948974609375},
   2: {0: 0.703948974609375},
   3: {0: 1.2799804687499998},
   4: {0: 1.519976806640625},
   5: {0: 1.519976806640625},
   6: {0: 0.83595703125}
  }
