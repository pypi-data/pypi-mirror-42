import cwlbrowser.util as util

class Workflow:
	def __init__(self, name):
		self.name = name;
		self.inputs = []
		self.steps = []
		self.outputs = []
		self.graph = {}		


class Step:
	def __init__(self, name, in_, run, out, workflowGraph):
		self.name = name
		self.inputs = util.instantiateInputs(in_, workflowGraph, step=True, stepName=name)
		self.outputs = util.instantiateOutputs(out, workflowGraph, step=True)
		self.run = run

	def __str__(self):
		return "Step: {0} | Run: {1}".format(self.name, self.run)

class Input:
	def __init__(self, name, type, source="WORKFLOW"):
		self.name = name
		self.type = type
		self.source = source

	def __str__(self):
		return "Input: {0} | Type: {1}".format(self.name, self.type)

class Output:
	def __init__(self, name, type, source="WORKFLOW"):
		self.name = name
		self.type = type
		self.source = source

	def __str__(self):
		return "Output: {0} | Type: {1}".format(self.name, self.type)