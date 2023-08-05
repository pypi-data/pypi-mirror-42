############################################################################
# Copyright ESIEE Paris (2018)                                             #
#                                                                          #
# Contributor(s) : Benjamin Perret                                         #
#                                                                          #
# Distributed under the terms of the CECILL-B License.                     #
#                                                                          #
# The full license is in the file LICENSE, distributed with this software. #
############################################################################

import higra as hg


@hg.argument_helper(hg.CptEdgeWeightedGraph)
def labelisation_watershed(edge_weights, graph):
    """
    Compute a watershed cut of the given edge weighted graph.

    The watershed cut is represented by a labelisation of the graph vertices.

    :param edge_weights: Weights on the edges of the graph (Concept :class:`~higra.CptEdgeWeightedGraph`)
    :param graph: (deduced from :class:`~higra.CptEdgeWeightedGraph`)
    :return: A labelisation of the graph vertices (Concept :class:`~higra.CptVertexWeightedGraph`)
   """
    vertex_labels = hg._labelisation_watershed(graph, edge_weights)

    vertex_labels = hg.delinearize_vertex_weights(vertex_labels, graph)
    hg.CptVertexLabeledGraph.link(vertex_labels, graph)

    return vertex_labels
