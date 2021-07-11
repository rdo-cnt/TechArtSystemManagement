



def prepSaveSourceFileForAsset(dagPath):
	"""Prepares source file for the asset

	:param dagPath: DAG path
	:type dagPath: string
	"""
	# get node name
	node = dagPath.split('|')[-1]

	# make sure to set the node to world
	MC.parent(dagPath, w=True)

	# delete everything else
	delNodes = [x for x in MC.ls(dag=True, l=True) if not x.startswith('|{}'.format(node))]
	cams = ['persp', 'top', 'front', 'side']
	for cam in cams:
	    delNodes = [x for x in delNodes if not x.startswith('|{}'.format(cam))]
	MC.delete(delNodes)


	# make sure transforms are default
	attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
	for attr in attrs:
	    MC.setAttr('{}.{}'.format(node, attr), 0)
	attrs = ['sx', 'sy', 'sz']
	for attr in attrs:
	    MC.setAttr('{}.{}'.format(node, attr), 1)