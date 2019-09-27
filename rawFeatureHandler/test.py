import pickle
import matplotlib.pyplot as plt
import networkx as nx

with open('../rawFeatures/linuxkernel-arm-O2v54/verify_test.ida', 'r') as f:
	bb=pickle.load(f)
	f.close()
	for nxg in bb.get_graphs():
		#if nxg.funcname == 'group_order_tests':
		if nxg.funcname == 'verify_detached_signature_cert':

			G = nxg.g

			break
	print G


	#pos = nx.spring_layout(G)

	nx.draw(G)
	#node_labels = nx.get_node_attributes(G,'state')
	#nx.draw_networkx_labels(G, pos, labels = node_labels)
	#edge_labels = nx.get_edge_attributes(G,'state')
	#nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)

	plt.savefig('this.png')
	plt.show()