
from xMaya.reps import utils
reload(utils)





@utils.timeit
def write(fullLodRepPath, sourceFile, framestart, frameend):
	utils.openAndPrepSourceFile(sourceFile)
	utils.MC.select('|base')
	utils.MC.file('{}/{}.obj'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME), force=True, options='groups=1;ptgroups=1;materials=0;smoothing=1;normals=1', typ='OBJexport', es=True)

@utils.timeit
def load(assetName, fullLodRepPath):
	fullLodRepPath = '{}/{}.obj'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME)
	utils.objImport(assetName, fullLodRepPath)
