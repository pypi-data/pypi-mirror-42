import requests
import base64
import yaml
import os
import cwltool
import subprocess
import cwlbrowser.workflow as wf
import cwlbrowser.util as util
from IPython.display import SVG, display
import time
import os


out_workflow = {}
steps = []
STEPS_WEIGHTING = 70
IO_WEIGHTING = 15

def retrieveFileThruLink(link, path):
	req = requests.get(link)
	if req.status_code != 200:
	    print(req.status_code)
	    if req.status_code == 404:
	    	print ("cwl file not found. Maybe due to incorrect url")
	    	print("\n")
	else:
		req = req.json()  	    
		content = base64.b64decode(req['content'])
		content = content.decode("utf-8")
		try:
			out_workflow = yaml.safe_load(content)
			#print (out_workflow)
			return createWorkflowObject(path, out_workflow)
		except (yaml.YAMLError) as yamlError:
			print ("Error in loading the cwl file")
			print (yamlError)

#If you are passing the workflow argument as a link make sure that you also
#pass the argument True to indicate that
def load(workflow, link=False):
	if(link == False):
		global out_workflow
		if os.path.exists(workflow):
			file = open(workflow, 'rb')
			try:
				out_workflow = yaml.safe_load(file)
				return createWorkflowObject(workflow, out_workflow)
			except (yaml.YAMLError):
				print ("Error in loading the cwl file")
		else:
			print("File not located")
			return -1;
	else:
		return loadWithLink(workflow)

#loads workflow when given full url
def loadWithLink(link) :
	lhs, rhs = link.split("/blob/", 1)
	branch, path = rhs.split("/", 1)
	ownerrepo = lhs.replace('https://github.com', "")
	finallink = "https://api.github.com/repos" + ownerrepo + "/contents/" + path
	return retrieveFileThruLink(finallink, path)






#print the specified attribute you want 
#pass the attribute as a string to the method
#E.G. printWorfklow("inputs")
def printWorkflowAttr(attribute) :
	if attribute in out_workflow.keys() :
		print(attribute + ":")
		for item in out_workflow[attribute] :
			print (item)
		print ("\n")
	else :
		print("No such attribute as: " + attribute + " found in workflow")

#creates workflow object from dict
def createWorkflowObject(name, workflow) :
	workflowObject = wf.Workflow(name)
	workflowObject.inputs = util.instantiateInputs(workflow["inputs"], workflowGraph=workflowObject.graph)
	workflowObject.steps = instantiateSteps(workflow["steps"], workflowObject.graph)
	workflowObject.outputs = util.instantiateOutputs(workflow["outputs"], workflowGraph=workflowObject.graph)
	return workflowObject


def displayGraphSVG(workflow, type="link"):
	if (type  == "link") :
		BASE_URL = 'https://view.commonwl.org'

		HEADERS = {
		    'user-agent': 'my-app/0.0.1',
			'accept': 'application/json'
		}

		addResponse = requests.post(BASE_URL + '/workflows', 
								data={'url': workflow},		
								headers=HEADERS)
		if (addResponse.status_code == 200) :
			postExistingWorkflowGraph(workflow)
		elif (addResponse.status_code == requests.codes.accepted):
			qLocation = addResponse.headers['location']

			# Get the queue item until success
			qResponse = requests.get(BASE_URL + qLocation,
									headers=HEADERS,
									allow_redirects=False)
			maxAttempts = 5
			while qResponse.status_code == requests.codes.ok and qResponse.json()['cwltoolStatus'] == 'RUNNING' and maxAttempts > 0:
				time.sleep(5)
				qResponse = requests.get(BASE_URL + qLocation,
										headers=HEADERS,
										allow_redirects=False)
				maxAttempts -= 1
			if 'location' in qResponse.headers:
			# Success, get the workflow
				workflowResponse = requests.get(BASE_URL + qResponse.headers['location'], headers=HEADERS)
				if (workflowResponse.status_code == requests.codes.ok):
					workflowJson = workflowResponse.json()
					# Do what you want with the workflow JSON
					# Include details in documentation files etc
					display(SVG(BASE_URL + workflowJson['visualisationSvg']))
				else:
					print('Could not get returned workflow')
			elif (qResponse.json()['cwltoolStatus'] == 'ERROR'):
				# Cwltool failed to run here
				print(qResponse.json()['message'])
			elif (maxAttempts == 0):
				print('Timeout: Cwltool did not finish')
			else :
				print('Something is not right')

		else:
			print (addResponse.status_code)
			print('Error adding workflow')
	elif (type== "file"):
		name, suffix = workflow.split(".cwl") 
		p = subprocess.run(["cwltool", "--print-dot", workflow], capture_output=True)
		if(p.returncode != 0) :
			print ("Something went wrong")
			print(bytes.decode(p.stderr))
		else :
			graphFile = name + ".svg"
			display(SVG(graphFile))
	else :
		print("Invalid type")

	"""
	"""
def postExistingWorkflowGraph(link) :
	BASE_URL = 'https://view.commonwl.org'

	HEADERS = {
		'accept': 'application/json'
	}
	shortenedLink = link.replace("https://", "")
	finishedlink = BASE_URL + "/workflows/" + shortenedLink
	req = requests.get(finishedlink, headers=HEADERS)
	if req.status_code != 200:
		print(req.status_code)
	else:
		req = req.json()     
		display(SVG(BASE_URL + req['visualisationSvg']))


def compareNoOfInputs(workflow1, workflow2):
    util.compare(workflow1.name, workflow2.name, workflow1.inputs, workflow2.inputs, "inputs")

def compareNoOfOutputs(workflow1, workflow2):
	util.compare(workflow1.name, workflow2.name, workflow1.outputs, workflow2.outputs, "outputs")

def compareNoOfSteps(workflow1, workflow2):
	util.compare(workflow1.name, workflow2.name, workflow1.steps, workflow2.steps, "steps")


def instantiateSteps(steps, workflowGraph) :
	temp = []
	#print (steps)
	if (isinstance(steps, dict)) :
		for key, value in steps.items() :
			item = wf.Step(key, value["in"], value["run"], value["out"], workflowGraph)
			workflowGraph[key] = []
			temp.append(item)
	else :
		for step in steps :
			stepObj = wf.Step(step["id"], step["in"], step["run"], step["out"], workflowGraph)
			workflowGraph[step["id"]] = []
			temp.append(stepObj)
	return temp

def similarityCheck(workflow1, workflow2):
	(stepSimilarity, diffSmall, diffBig, smallerWorkflow, biggerWorkflow) = similarityCheckSteps(workflow1, workflow2)
	print("SIMILARITY CHECK BETWEEN {} AND {}:".format(workflow1.name, workflow2.name))
	util.printItemSimilarityStats(diffSmall, diffBig, smallerWorkflow, biggerWorkflow, "STEPS")
	(inputSimilarity, diffSmall, diffBig, smallerWorkflow, biggerWorkflow) = similarityCheckInputs(workflow1, workflow2)
	util.printItemSimilarityStats(diffSmall, diffBig, smallerWorkflow, biggerWorkflow, "INPUTS")
	(outputSimilarity, diffSmall, diffBig, smallerWorkflow, biggerWorkflow) = similarityCheckOutputs(workflow1, workflow2)
	util.printItemSimilarityStats(diffSmall, diffBig, smallerWorkflow, biggerWorkflow, "OUTPUTS")
	overallSimilarity = stepSimilarity + inputSimilarity + outputSimilarity
	print("---------------------------------------------------------------------------------------")
	print("OVERALL MATCH: {}".format(overallSimilarity))
	print("---------------------------------------------------------------------------------------")
	print("\n")


def similarityCheckSteps(workflow1, workflow2):
	return util.similarityCheckItems(workflow1, workflow2, "steps" , STEPS_WEIGHTING)

def similarityCheckOutputs(workflow1, workflow2) :
	return util.similarityCheckItems(workflow1, workflow2, "outputs", IO_WEIGHTING)

def similarityCheckInputs(workflow1, workflow2) :
	return util.similarityCheckItems(workflow1, workflow2,"inputs", IO_WEIGHTING)









	
