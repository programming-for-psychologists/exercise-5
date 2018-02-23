import random
import itertools
import random
import sys
from psychopy import visual, core, event

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

def generateTrials(numTrials):
	trials=[]
	for i in range(numTrials):
		positionType = random.choice(positions.keys())
		targetCategory = random.choice(categories.keys())
		distractorCategories = randomButNot(categories.keys(),targetCategory,2)
		actorsToShow = random.sample(actors,3)
		targetLocation = random.choice(positions[positionType].keys())
		trials.append({
					'positionType':positionType,
					'emotionPrompt':targetCategory,
					'targetImage':actorsToShow[0]+categories[targetCategory]+suffix,
					'distractorImage1': actorsToShow[1]+categories[distractorCategories[0]]+suffix,
					'distractorImage2': actorsToShow[1]+categories[distractorCategories[1]]+suffix,
					'targetLocation': targetLocation
					})
	return trials


trials = generateTrials(80)
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
	while True:
		if mouse.isPressedIn(pic1) or mouse.isPressedIn(pic2) or mouse.isPressedIn(pic3):
			response = mouse.getPos()
			break

	win.flip()
	core.wait(.2)

	#check if response is correct
	if pic1.contains(response):
		correctFeedback.draw()
	else:
		incorrectFeedback.draw()
	win.flip()
	core.wait(.5)
