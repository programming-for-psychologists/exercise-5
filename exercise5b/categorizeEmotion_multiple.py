import random
import itertools
import random
import sys
import numpy as np
from psychopy import visual, core, event

categories = {'Happy':'F', 'Angry':'W', 'Sad':'T'}
actors = ['001m', '001w', '002m', '002w', '003m', '003w', '004m', '004w', '005m', '005w']
suffix = '_90_60.jpg'
positions = {'left':(-190,0), 'middle':(0,0), 'right':(190,0)}
responseMapping = {'left':'1','middle':'2','right':'3'}

def randomButNot(l,toExclude,num):
	chosen = random.sample(l,num)
	while toExclude in chosen:
		chosen = random.sample(l,num)
	return chosen

def generateTrials(numTrials):
	trials=[]
	for i in range(numTrials):
		targetCategory = random.choice(categories.keys())
		distractorCategories = randomButNot(categories.keys(),targetCategory,2)
		actorsToShow = np.random.choice(actors,3)
		targetLocation = random.choice(positions.keys())
		trials.append({
					'emotionPrompt':targetCategory,
					'targetImage':actorsToShow[0]+categories[targetCategory]+suffix,
					'distractorImage1': actorsToShow[1]+categories[distractorCategories[0]]+suffix,
					'distractorImage2': actorsToShow[2]+categories[distractorCategories[1]]+suffix,
					'targetLocation': targetLocation
					})
	return trials


trials = generateTrials(40)

win = visual.Window([1024,700],color="black", units='pix')
prompt = visual.TextStim(win=win,text='',color="white",height=60)
correctFeedback = visual.TextStim(win=win,text='CORRECT',color="green",height=60)
incorrectFeedback = visual.TextStim(win=win,text='ERROR',color="red",height=60)
pic1 = visual.ImageStim(win=win, mask=None,interpolate=True)
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True)
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True)

for curTrial in trials:
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
	pic1.setPos(positions[curTrial['targetLocation']])
	distractorPositions = randomButNot(positions.keys(),curTrial['targetLocation'],2)
	pic2.setPos(positions[distractorPositions[0]])
	pic3.setPos(positions[distractorPositions[1]])

	pic1.draw()
	pic2.draw()
	pic3.draw()
	win.flip()
	response = event.waitKeys(keyList=responseMapping.values())[0]
	print response,responseMapping[curTrial['targetLocation']]
	if response==responseMapping[curTrial['targetLocation']]:
		correctFeedback.draw()
	else:
		incorrectFeedback.draw()
	core.wait(.5)