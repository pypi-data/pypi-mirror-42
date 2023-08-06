
from compressing.graph.proof_graph import ProofGraph

import time
import random

# def run_experiments(dir_proofs):
#     path = dir_proofs + "/"
#     files = \
#         [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#
#     for proof in files
#
#     repeated_formulas = comp.get_nodes_repeated_formulas(self.proof)
#
#     collapse = 1
#     for level, repeated_nodes in repeated_formulas.items():
#         for nodes in repeated_nodes:
#             node_u = nodes.pop()
#             for node_v in nodes:
#                 rule_function = \
#                     comp.identify_rule(self.proof, node_u, node_v)
#                 node_u = comp.exec_rule(rule_function, self.proof, node_u,
#                                         node_v)
#                 collapse += 1
#
#     comp.redirect_multi_ancestor_edges(self.proof)
#     comp.demote_ancestor_edges(self.proof)
#     comp.remove_unused_colors(self.proof)
#
#     # self.visual_pg.draw_final(comp_file_path)


def compress(graph):

    proof_graph = ProofGraph(digraph=graph, init_data=True)

    exec_time = range(1, 5)

    time.sleep(random.choice(exec_time))

    return 5, 2
