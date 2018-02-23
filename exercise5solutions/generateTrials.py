import random
from useful_functions import *
import numpy as np


categories = {'Happy':'F', 'Angry':'W', 'Sad':'T'}
actors = ['001m', '001w', '002m', '002w', '003m', '003w', '004m', '004w', '005m', '005w']
suffix = '_90_60.jpg'
positions = {
			'vertical':  {'bottom':(-190,0), 'middle':(0,0), 'top':(190,0)},
			'horiontal': {'left':(0,-190), 'middle':(0,0), 'right':(0,190)}
			}



def generateTrials(subjCode,numTrials):

	var_order = ['subjCode','positionType','emotionPrompt',\
				'targetActor','distractor1Actor', 'distractor2Actor',\
				'distractorEmotion1', 'distractorEmotion2',\
				'targetImage', 'distractorImage1','distractorImage2','targetLocation']


	trials=[]
	trialFile = open('trials/'+subjCode+'_trials.csv','w')
	trialFile.write(','.join(var_order)+'\n')

	for i in range(numTrials):
		positionType = random.choice(positions.keys())
		targetCategory = random.choice(categories.keys())
		distractorCategories = randomButNot(categories.keys(),targetCategory,2)
		actorsToShow = np.random.choice(actors,3) # choose 3 WITH replacement (cf. random.choice() which chooses WITHOUT replacement)
		targetLocation = random.choice(positions[positionType].keys())

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
					'distractorImage2': actorsToShow[2]+categories[distractorCategories[1]]+suffix,
					'targetLocation': targetLocation
					})

		random.shuffle(trials)
	for curTrial in trials:
		trialData = [curTrial[curField] for curField in var_order]
		trialFile.write(','.join(trialData)+'\n')

	return var_order

if __name__ == '__main__':
	generateTrials("testSubj",100)
