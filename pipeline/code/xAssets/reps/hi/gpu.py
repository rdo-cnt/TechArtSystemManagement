
from xAssets.reps import utils
reload(utils)





@utils.timeit
def write(fullLodRepPath, sourceFile, framestart, frameend):
	pass

@utils.timeit
def load(assetName, fullLodRepPath):
	fullLodRepPath = '{}/{}.abc'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME)
	utils.abcGpuImport(assetName, fullLodRepPath)