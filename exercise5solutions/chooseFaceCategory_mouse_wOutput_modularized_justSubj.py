import random
import itertools
import random
import sys
import os
import numpy as np
from psychopy import visual, core, event, gui
from generateTrials import *
from useful_functions import *


numTrials = 100

while True:
	runTimeVarOrder = ['subjCode']
	runTimeVars = getRunTimeVars({'subjCode':'subjCode'},runTimeVarOrder)
	if runTimeVars['subjCode']=='':
		popupError('Need to enter a subject code')
	else:
		outputFile = open(runTimeVars['subjCode']+'_data.csv','w')
		break


var_order = generateTrials(runTimeVars['subjCode'],numTrials)
trials = importTrials('trials/'+runTimeVars['subjCode']+'_trials.csv',separator=",")

win = visual.Window([750,750],color="black", units='pix')
#win = visual.Window(fullscr=True,color="black", units='pix')
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
	writeToFile(outputFile,all_vars,writeNewLine=True) 	#write data to output file




