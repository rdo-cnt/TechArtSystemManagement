
from xAssets.reps import utils
reload(utils)





@utils.timeit
def write(fullLodRepPath, sourceFile, framestart, frameend):
	utils.openAndPrepSourceFile(sourceFile)
	utils.prepLow()
	utils.MC.AbcExport(j='-frameRange {} {} -dataFormat ogawa -root |base -file {}/{}.abc'.format(framestart, frameend, fullLodRepPath, utils.assetConfig.SOURCEFILENAME))


@utils.timeit
def load(assetName, fullLodRepPath):
	fullLodRepPath = '{}/{}.abc'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME)
	utils.abcImport(assetName, fullLodRepPath)