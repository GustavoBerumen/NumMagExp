#!/usr/bin/env python2
'''
An application for a psychology experiment concerning number discrimination using PsychoPy2.

Displays a series of trials. Each trial contains two arrays of dots on opposite sides of the screen and awaits user input. 
Input indicates which side the user thinks has more elements. The time to respond, number of elements on each side, 
and whether the response is correct are recorded for each trial. The data is returned as a dictionary and printed to the 
screen. Most important parameters such as number of trials are stored in global variables and can be altered from there.

Written by Max Spiegel & Gustavo Berumen, Dec, 2014 (in progress). 
'''
from psychopy import core, visual, event, sound, gui, data, logging
from random import random, choice
import numpy 
import os


# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(thisDir)
# ########### GLOBAL VARIABLES # ########### 

NUM_TRIALS = 2 #default number of trials per experiment
N_REPS = 2 #default number of repetitions of each trial

MAX_WAIT = 2 #maximum response time
FEED_WAIT= 1 #feedback waiting time
DOTS_WAIT = 1 #dots waiting time on screen
 
WIDTH = 1366 #Screen width and height in pixels as global variables.
HEIGHT = 768

XLIM1 = 0.2 #x and y limits of dot array in normal units [?]
XLIM2 = 0.8
YLIM = 0.7

MAX_RADIUS = 30 #max and min radii of dots
MIN_RADIUS = 20

MAX_DOTS = 10 #max and min number of dots
MIN_DOTS = 1

EXT_DIST = 20 #extra distance factor as percentage. 


# ########### FUNCTIONS # ########### 
def refresh(myWin):
    myWin.flip()
    fixation()
    core.wait(0.5)
    myWin.flip()
    core.wait(0.25)


def mask():
       
    '''
    input: none
    displays a mask to prevent after images effects
    returns: none
    '''
    myTex = numpy.random.random((256,256))
    myStim = visual.GratingStim(myWin, tex=myTex, size=[WIDTH,HEIGHT], opacity=1.0)
    myStim.draw()
    myWin.flip()


def fixation():
    '''
    input: none
    displays a cross hairs and plays a beep
    returns: none
    '''
    lar=24
    sz = numpy.array([lar, lar])
    barX = visual.Line(myWin, start=(sz*-1), end=sz, ori=45,\
                        pos=[0, 0], lineWidth=6, lineColor=(1,1,1))
    barY = visual.Line(myWin, start=(sz*-1), end=sz, ori=135,\
                        pos=[0, 0], lineWidth=6, lineColor=(1,1,1))
    beep = sound.Sound(value = 4000, secs=0.25)
    barX.draw()
    barY.draw()
    myWin.flip()
    beep.play()


def information(): 
    # Store info about the experiment session
    expName = 'numMagExp'
    expInfo = {'nombre':'jwp', 'edad':'12', 'sexo':['mas','fem']}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: 
        core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName

    # Define a textbox which appears in case of error(s) at typing participant's information 
    myDlg = gui.Dlg(title="Error")
    myDlg.addText('Ingresa la informacion correctamente', color='Blue')
    myDlg.addText('Ejemplo:')
    myDlg.addFixedField(label='edad', value='12')
    myDlg.addFixedField(label='nombre', value='jpma')
    myDlg.addText('') # [?]
    myDlg.addText('Intenta de nuevo')
    
    # Only pass if participants information has been properly written
    try:
        int(expInfo['nombre']) # throws ValueError if 'name' is not an integer 
        myDlg.show() # else throws 'NameError' and quits if name is integer
        raise NameError("Participant information entered incorrectly.")
        core.quit()
    except ValueError: # enters block if name is not an integer
        try: # throws error if 'edad' is string, if field is blank or age less than zero
            if len(expInfo['nombre']) == 0 or int(expInfo['edad']) <= 0: 
                raise ValueError
        except ValueError:
            myDlg.show()
            raise ValueError("Participant information entered incorrectly.")
            core.quit()
            
    return expInfo


def buildTrialList(nTrials, expInfo):
    ######################
    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    fileName=thisDir+os.sep+u'datos'+os.sep+'/%s_%s_%s'%(expInfo['nombre'],expInfo['expName'],expInfo['date'])
    
    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expInfo['expName'], version='draft',
                                    extraInfo=expInfo, runtimeInfo=None,
                                    originPath=None,
                                    savePickle=True, saveWideText=True,
                                    dataFileName=fileName)
    #save a log file for detail verbose info
    logFile = logging.LogFile(fileName+'.log', level=logging.WARNING)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
    
    ######################
    try:
        trialList = data.importConditions(thisDir+os.sep+u'conds'+os.sep+'trialTypes.xlsx')
    except:
        trialList = []
        for trial in range(nTrials):
            trialList += [{
                'name': expInfo['nombre'],
                'age': expInfo['edad'],
                'gender': expInfo['sexo'],
                'lDots': '',
                'rDots': '',
                'lColor': '',
                'rColor': ''
            }]
        
    trials = data.TrialHandler(nReps=N_REPS, method='random', 
                                extraInfo=expInfo, originPath=None,
                                trialList=trialList,
                                seed=None, name='trials')
    trials.setExp(thisExp)
    return trials, thisExp, fileName


def instructions():
    '''
    input: none
    displays a message for the participants about the content of the task
    returns: none
    '''
    mess_1= u'\xa1Hola! \n\nEn las imagenes que veras, responde: \n\n\xbfCual de los grupos de puntos tiene mas puntos?\n\nLos de la\n        IZQUIERDA (presiona flecha izquierda)\n        DERECHA   (presiona flecha derecha)'
    mess_2= u'Presiona "Espacio" para continuar'
    instr_1 = visual.TextStim(myWin, text=mess_1, font='Helvetica',\
                pos=(0, 30), color=(1,1,1), height=32, wrapWidth =800)
    instr_2 = visual.TextStim(myWin, text=mess_2,  font='Helvetica',\
                pos=(0, -350), color=(1,1,1), height=20, wrapWidth =800)
    
    instr_1.draw()
    instr_2.draw()
    myWin.flip()
    
    key=['']
    while key[0] not in ['space']:
        key = event.waitKeys()
        if key[0] in ['escape']:
            core.quit()
    event.clearEvents()


def makeNewDot(trials,dots,lColor,rColor,rDots,xLim1=XLIM1,xLim2=XLIM2,\
                    yLim=YLIM,minRad=MIN_RADIUS,maxRad=MAX_RADIUS,):
    '''
    inputs: list of dots and int number of fields on right side of partition.
    Generates position and randomly randomly within bounds
    returns: new instance of Circle object
    '''
    size = (maxRad-minRad)*random() + minRad
    if len(dots) < rDots: #if still populating right side
        pos = ((xLim2-xLim1)*random() + xLim1) * WIDTH/2.0,\
               (2*yLim*random() - yLim) * HEIGHT/2.0
        color = rColor
    else: #otherwise populating left side
        pos = -((xLim2-xLim1)*random() + xLim1) * WIDTH/2.0,\
               (2*yLim*random() - yLim) * HEIGHT/2.0
        color = lColor
    return visual.Circle(myWin, edges=64, fillColor=color, lineColor=color,\
                            pos=pos, radius=size)
                            

def overlap(dot1, dot2):
    '''
    inputs: dot1 and dot2 are Circle objects. 
    The sizes and positions of the dots are checked to determine if they overlap.
    returns: boolean True if overlap, False otherwise
    '''
    #if distance between centers is less than sum of radii they overlap [?]
    if ((dot1.pos[0]-dot2.pos[0])**2+(dot1.pos[1]-dot2.pos[1])**2)**0.5\
                    < (1 + float(EXT_DIST)/100)*(dot1.radius+dot2.radius):
        return True
    return False
def drawArray(trials,minDots=MIN_DOTS,maxDots=MAX_DOTS,extDist=EXT_DIST):
    '''
    intputs: int number of dots on left and right
    renders dot array image according to parameters given by global variables
    returns: none
    '''
    #if no xlsx file with conditions
    if trials.thisTrial['lDots'] == '':
        # generate range of dots
        n = range(minDots, maxDots + 1)
        trials.thisTrial['rDots'] = choice(n)
        n.remove(trials.thisTrial['rDots'])
        trials.thisTrial['lDots'] = choice(n)
        
        #generate a random color for each set of dots
        trials.thisTrial['lColor'] = (2*random()-1,2*random()-1,2*random()-1)
        trials.thisTrial['rColor'] = (2*random()-1,2*random()-1,2*random()-1)
    
    lDots = trials.thisTrial['lDots']
    rDots = trials.thisTrial['rDots']
    lColor = trials.thisTrial['lColor']
    rColor = trials.thisTrial['rColor']
    
    #initialize first dot and add to list of dots
    dots = []
    dots.append(makeNewDot(trials, dots, lColor, rColor, rDots))
    
    for count in range(rDots+lDots-1):
        #initialize next dot to be added
        newDot = makeNewDot(trials, dots, lColor, rColor, rDots)
        checked = 0 #initialize checked counter to zero
        
        #check against each other dot in place
        while checked < len(dots):
            if overlap(dots[checked], newDot): #if dots overlap
                #create new dot and start count over
                newDot = makeNewDot(trials, dots, lColor, rColor, rDots)
                checked = 0
            #otherwise check next dot       
            else:
                checked += 1
        #if no overlaps, add dot to list
        dots.append(newDot)
        
    #draw dots
    for dot in dots:
        dot.draw()
        

    #draw partition
    visual.Line(myWin, start=(0,-HEIGHT/2.0), end=(0,HEIGHT/2.0),\
                lineColor=-1, lineWidth=10).draw()
    #flip window
    myWin.flip()
    


def getResponse(trials, timer):
    '''
    inputs: dictionary of trial data so far
    awaits user input and records response
    returns: updated trial dictionary
    TODO: store response in expInfo
    '''
    
    #create feedbacks 
    feed_non=(visual.TextStim(myWin, text='No Respuesta', font='Helvetica',\
                pos=(0, 0), color=(1,1,1), height=40, wrapWidth =800))
    feed_cor=(visual.TextStim(myWin, text='Correcto', font='Helvetica',\
                pos=(0, 0), color=(1,1,1), height=40, wrapWidth =800))
    feed_inc=(visual.TextStim(myWin, text='Incorrecto', font='Helvetica',\
                pos=(0, 0), color=(1,1,1), height=40, wrapWidth =800))
                
    #reset timer and await valid response
    rTimer = timer.reset() 
    key=['']
    while 'left' not in key and 'right' not in key and rTimer < DOTS_WAIT:
        key = event.waitKeys(maxWait=DOTS_WAIT)
        if key == None:
            break
        if 'escape' in key or 'q' in key:
            core.quit()
#    event.clearEvents()
    if 'q' in key or 'escape' in key:
        core.quit()
    if key == None or 'left' not in key and 'right' not in key:
        key = ['']
        while 'left' not in key and 'right' not in key and rTimer < MAX_WAIT-DOTS_WAIT:
            key = event.waitKeys(maxWait=MAX_WAIT-DOTS_WAIT)
            if key == None:
                feed = feed_non
                myWin.flip()
                feed.draw()
                core.wait(FEED_WAIT)
                myWin.flip()
                trials.addData('respTime', None)
                trials.addData('correct', None)
                return
            if 'escape' in key or 'q' in key:
                core.quit()
#    allKeys = event.waitKeys(maxWait=DOTS_WAIT) #check for input while dots are onscreen
#    '''there is a bug here when a button is pressed while dots are onscreen'''
#    if  not ('right' in allKeys or 'left' in allKeys\
#                                or 'q' in allKeys or 'escape' in allKeys):
#        myWin.flip() #check for inputs after dots have left screen
#        allKeys = event.waitKeys(maxWait=(MAX_WAIT-DOTS_WAIT))
#
#    #Check if the keys we care about are in there, if not keeep waiting the diference
#    if allKeys == None or not ('right' in allKeys or 'left' in allKeys\
#                                or 'q' in allKeys or 'escape' in allKeys):
        
    
    #save response time and dot ratio
    trials.addData('respTime', timer.getTime())
    
    #check input and update trial dictionary
    for thisKey in key:
        if thisKey == 'left': #correct
            if trials.thisTrial['rDots'] < trials.thisTrial['lDots']:
                trials.addData('correct', True)
                feed = feed_cor

            else: #incorrect
                trials.addData('correct', False)
                feed = feed_inc
                
        elif thisKey == 'right': #correct
            if trials.thisTrial['rDots'] > trials.thisTrial['lDots']:
                trials.addData('correct', True)
                feed = feed_cor
                
            else: #incorrect
                trials.addData('correct', False)
                feed = feed_inc
                
        elif thisKey in ['q', 'escape']:
            core.quit() #abort experiment
               
    #flip window
    timer.reset()
    while timer.getTime() <= FEED_WAIT:
        myWin.flip()
        feed.draw()
    myWin.flip()

    return trials               


def farewell():
    '''
    input: none
    displays a message for the participants about the content of the task
    returns: none
    '''
    mess_1= u'\xa1Muchas gracias por participar! \n\n                   :-)'
    mess_2= u'Presiona cualquier tecla o espera unos segundos para salir'
    bye_1 = visual.TextStim(myWin, text=mess_1, font='Helvetica',\
            pos=(0, 0), color=(1,1,1), height=36, wrapWidth =800)
    bye_2 = visual.TextStim(myWin, text=mess_2,  font='Helvetica',\
            pos=(0, -350), color=(1,1,1), height=18, wrapWidth =800)
    bye_1.draw()
    bye_2.draw()
    myWin.flip()
    event.waitKeys(maxWait=6)
    event.clearEvents()


def runExperiment(expInfo, nTrials=NUM_TRIALS, minDots=MIN_DOTS, maxDots=MAX_DOTS):
    '''
    inputs: subject and experiment info, ints number of trials, min and max number of dots
    runs nTrials trials and stores the data from each trial in a dictionary. 
    Saves data as csv and xlsx
    returns: None
    '''   
    #initialize timer, trial data dict, and count
    timer = core.Clock()

    trials, thisExp, fileName = buildTrialList(nTrials, expInfo)
    
    instructions()
    for trial in trials: 
        refresh(myWin)
        drawArray(trials) # choose number of left and right dots randomly
        getResponse(trials, timer) #draw dot arrays and record response
        core.wait(0.5)
        myWin.flip()
        mask()
        core.wait(0.25)  
        thisExp.nextEntry()

    #Control the colons we will have in the Excel sheet
    trials.saveAsExcel(fileName=fileName,stimOut=['lDots','rDots','lColor','rColor'],\
                        dataOut=['correct_raw','respTime_raw','respTime_mean','respTime_std','order_raw'])
    
    farewell()
    
    return trials


# ########### START EXPERIMENT # ###########

# Initialize TextBox, in order to ask participant's information
expInfo = information()

#initialize window with default view fullscreen and units pixels
myWin=visual.Window((WIDTH, HEIGHT), monitor='asus',\
                    fullscr=True, units="pix", color=[-0,0,0])

runExperiment(expInfo)


'''
**THINGS TO DO**
BUGGY:Does not save info for repetitions separately in Excel file.
    #OPTIONAL
Add motion to the dots
Present stimulus non-target before the dots (e.g. a square and a triangle)
Control the total area and individual area of the circles
'''
