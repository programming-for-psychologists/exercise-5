import random
import os
from psychopy import visual, core, gui


def randomButNot(l,toExclude,num):
	chosen = random.sample(l,num)
	while toExclude in chosen:
		chosen = random.sample(l,num)
	return chosen


def popupError(text):
	errorDlg = gui.Dlg(title="Error", pos=(400,400))
	errorDlg.addText('Error: '+text, color='Red')
	errorDlg.show()



def writeToFile(fileHandle,trial,separator=',', sync=True,writeNewLine=False):
	"""Writes a trial (array of lists) to a previously opened file"""
	line = separator.join([str(i) for i in trial]) #separate by separator (normally comma or tab)
	if writeNewLine:
		line += '\n' #add a newline
	try:
		fileHandle.write(line)
	except:
		print 'file is not open for writing'
	if sync:
			fileHandle.flush()
			os.fsync(fileHandle)



def openOutputFile(subjCode):
	if  os.path.isfile(subjCode+'_data.txt'):
		popupError('Error: That subject code already exists')
		return False
	else:
		try:
			outputFile = open(subjCode+'_data.txt','w')
		except:
			print 'could not open file for writing'
		return outputFile



def getRunTimeVars(varsToGet,order):
	"""Get run time variables, see http://www.psychopy.org/api/gui.html for explanation"""
	infoDlg = gui.DlgFromDict(dictionary=varsToGet, order=order)	
	if infoDlg.OK:
		return varsToGet
	else: print 'User Cancelled'



def importTrials(trialsFilename, colNames=None, separator='\t'):
	try:
		trialsFile = open(trialsFilename, 'rb')
	except IOError:
		print trialsFilename, 'is not a valid file'
	
	if colNames is None: # Assume the first row contains the column names
		colNames = trialsFile.next().rstrip().split(separator)
	trialsList = []
	for trialStr in trialsFile:
		trialList = trialStr.rstrip().split(separator)
		assert len(trialList) == len(colNames)
		trialDict = dict(zip(colNames, trialList))
		trialsList.append(trialDict)
	return trialsList

