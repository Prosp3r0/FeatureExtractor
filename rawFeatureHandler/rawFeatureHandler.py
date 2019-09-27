import pickle
import matplotlib.pyplot as plt
import networkx as nx
import os
import json

rawFeatures_path = '/Users/Max/Documents/capstone/FeatureResource/rawFeatures/'

class rawHandler():
	def __init__(self, ida_file, error):
		self.ida_filepath = ida_file
		self.error = error

	def extractFromGraphs(self):
		if os.path.dirname(self.ida_filepath) + '/' == rawFeatures_path:
			return None
		print('[+] Extracting features: {}'.format(self.ida_filepath))
		with open(self.ida_filepath, 'r') as f:
			try:
				bb = pickle.load(f)
			except Exception as e:
				self.error.append(e)
				return None
			f.close()
			result = []
			for nxg in bb.get_graphs():
				func = {}
				func['features'] = []
				func['fname'] = ''
				func['src'] = ''
				func['succs'] = []
				func_graph = nxg.old_g
				func['n_num'] = len(func_graph.nodes)
				for i in range(0, func['n_num']):
					node_feature = []
					#node_feature.append(node['numLIs'])
					node_feature.append(float(func_graph.nodes[i]['numAs']))
					node_feature.append(float(func_graph.nodes[i]['offs']))
					node_feature.append(float(len(func_graph.nodes[i]['strings'])))
					node_feature.append(float(len(func_graph.nodes[i]['consts'])))
					node_feature.append(float(func_graph.nodes[i]['numTIs']))
					node_feature.append(float(func_graph.nodes[i]['numCalls']))
					node_feature.append(float(func_graph.nodes[i]['numIns']))

					func['features'].append(node_feature)

				for i in range(0, func['n_num']):
					node_succ = []
					for nbr, datadict in func_graph.succ[i].items():
						node_succ.append(nbr)
					func['succs'].append(node_succ)

				func['src'] = os.path.dirname(self.ida_filepath)[len(rawFeatures_path):] + '/' + \
							  os.path.splitext(os.path.basename(self.ida_filepath))[0]
				func['fname'] = nxg.funcname
				func_str = json.dumps(func)
				result.append(func_str)
			return result

'''
if __name__ == '__main__':
	rel = rawHandler('../rawFeatures/linuxkernel-arm-O2v54/verify_test.ida').extractFromGraphs()
	print('finished')
'''


