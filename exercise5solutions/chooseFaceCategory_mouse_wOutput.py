import random
import itertools
import random
import sys
import os
import numpy as np
from psychopy import visual, core, event,gui

categories = {'Happy':'F', 'Angry':'W', 'Sad':'T'}
actors = ['001m', '001w', '002m', '002w', '003m', '003w', '004m', '004w', '005m', '005w']
suffix = '_90_60.jpg'
positions = {
			'vertical':  {'bottom':(-190,0), 'middle':(0,0), 'top':(190,0)},
			'horiontal': {'left':(0,-190), 'middle':(0,0), 'right':(0,190)}
			}

def randomButNot(l,toExclude,num):
	chosen = random.sample(l,num)
	while toExclude in chosen:
		chosen = random.sample(l,num)
	return chosen


def popupError(text):
	errorDlg = gui.Dlg(title="Error", pos=(400,400))
	errorDlg.addText('Error: '+text, color='Red')
	errorDlg.show()


def generateTrials(subjCode,numTrials):
	trials=[]
	for i in range(numTrials):
		positionType = random.choice(positions.keys())
		targetCategory = random.choice(categories.keys())
		distractorCategories = randomButNot(categories.keys(),targetCategory,2)
		actorsToShow = np.random.choice(actors,3) # choose 3 WITH replacement (cf. random.choice() which chooses WITHOUT replacement)
		targetLocation = random.choice(positions[positionType].keys())
		var_order = ['subjCode','positionType','emotionPrompt',\
					'targetActor','distractor1Actor', 'distractor2Actor',\
					'distractorEmotion1', 'distractorEmotion2',\
					'targetImage', 'distractorImage1','distractorImage2','targetLocation']

		trials.append({
					'subjCode':subjCode,
					'positionType':positionType,
					'emotionPrompt':targetCategory,
					'targetActor':actorsToShow[0],
					'distractor1Actor':actorsToShow[1],
					'distractor2Actor':actorsToShow[2],
					'distractorEmotion1':distractorCategories[0],
					'distractorEmotion2':distractorCategories[1],
					'targetImage':actorsToShow[0]+categories[targetCategory]+suffix,
					'distractorImage1': actorsToShow[1]+categories[distractorCategories[0]]+suffix,
					'distractorImage2': actorsToShow[1]+categories[distractorCategories[1]]+suffix,
					'targetLocation': targetLocation
					})
	return var_order,trials


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


while True:
	runTimeVarOrder = ['subjCode','gender']
	runTimeVars = getRunTimeVars({'subjCode':'', 'gender':['Choose', 'male','female','other']},runTimeVarOrder)
	if runTimeVars['subjCode']=='':
		popupError('Need to enter a subject code')
	elif 'Choose' in runTimeVars.values():
		popupError('Need to choose a value from a dropdown box')
	else:
		outputFile = openOutputFile(runTimeVars['subjCode'])
		if outputFile:
			break


var_order,trials = generateTrials(runTimeVars['subjCode'],100)
win = visual.Window([750,750],color="black", units='pix')
mouse = event.Mouse(win=win)
prompt = visual.TextStim(win=win,text='',color="white",height=60)
correctFeedback = visual.TextStim(win=win,text='CORRECT',color="green",height=60)
incorrectFeedback = visual.TextStim(win=win,text='ERROR',color="red",height=60)
pic1 = visual.ImageStim(win=win, mask=None,interpolate=True)
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True)
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True)

for curTrial in trials:
	distractorPositions = randomButNot(positions[curTrial['positionType']].keys(),curTrial['targetLocation'],2)

	#generate x,y coordinates for the target and two distractors based on positionType and the named locations in generateTrials
	picPositions = {
					'target': 		positions[curTrial['positionType']][curTrial['targetLocation']],
					'distractor1' : positions[curTrial['positionType']][distractorPositions[0]],
					'distractor2' :	positions[curTrial['positionType']][distractorPositions[1]]
					}


	win.flip()
	core.wait(.25)
	prompt.setText(curTrial['emotionPrompt'])
	prompt.draw()
	win.flip()
	core.wait(.5)

	win.flip()
	core.wait(.1)
	pic1.setImage('faces/'+curTrial['targetImage'])
	pic2.setImage('faces/'+curTrial['distractorImage1'])
	pic3.setImage('faces/'+curTrial['distractorImage2'])

	pic1.setPos(picPositions['target'])
	pic2.setPos(picPositions['distractor1'])
	pic3.setPos(picPositions['distractor2'])


	pic1.draw()
	pic2.draw()
	pic3.draw()
	win.flip()

	#check mouse until pressed in one of the pics
	responseTimer = core.Clock()
	while True:
		if mouse.isPressedIn(pic1) or mouse.isPressedIn(pic2) or mouse.isPressedIn(pic3):
			response = mouse.getPos()
			RT = responseTimer.getTime()*1000
			break

	win.flip()
	core.wait(.2)

	#check if response is correct
	isRight = int(pic1.contains(response))
	if isRight:
		correctFeedback.draw()
		emotionChosen = curTrial['emotionPrompt']
	else:
		incorrectFeedback.draw()
		if pic2.contains(response):
			emotionChosen = curTrial['distractorEmotion1']
		elif pic3.contains(response):
			emotionChosen = curTrial['distractorEmotion2']

	win.flip()
	core.wait(.5)


	independent_vars = [curTrial[curField] for curField in var_order]
	dependent_vars = [isRight,emotionChosen,RT]
	all_vars = independent_vars+dependent_vars
	print all_vars
	writeToFile(outputFile,all_vars,writeNewLine=True) 	#write data to output file




