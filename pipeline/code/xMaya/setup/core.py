
import maya.OpenMaya as OM
import callbacks
import os


def mayaInit(input):
    print '- running mayaInit callback'
    reload(callbacks)
    callbacks.mayaInitCallback()

def preSceneSave(input):
    print '- running preSceneSave callback'
    reload(callbacks)
    callbacks.preSceneSaveCallback()

def postSceneSave(input):
    print '- running postSceneSave callback'
    reload(callbacks)
    callbacks.postSceneSaveCallback()
    
def preSceneOpen(input):
    print '- running preSceneOpen callback'
    reload(callbacks)
    callbacks.preSceneOpenCallback()

def postSceneOpen(input):
    print '- running postSceneOpen callback'
    reload(callbacks)
    callbacks.postSceneOpenCallback()

def setupCallbacks():
    mayaInitCB      = OM.MSceneMessage.addCallback(OM.MSceneMessage.kMayaInitialized,mayaInit)
    preSceneSaveCB  = OM.MSceneMessage.addCallback(OM.MSceneMessage.kBeforeSave,preSceneSave)
    postSceneSaveCB = OM.MSceneMessage.addCallback(OM.MSceneMessage.kAfterSave,postSceneSave)
    preSceneOpenCB  = OM.MSceneMessage.addCallback(OM.MSceneMessage.kBeforeOpen,preSceneOpen)
    postSceneOpenCB = OM.MSceneMessage.addCallback(OM.MSceneMessage.kAfterOpen,postSceneOpen)

def setupGlobals():
    os.environ['ACTIVE_PROJECT'] = ''
    os.environ['ACTIVE_BLOCK']   = ''

# KEEP ON BOTTOM OF MODULE
def mainSetup():
    setupGlobals()
    setupCallbacks()