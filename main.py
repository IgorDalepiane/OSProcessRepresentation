import sys
import time
import random
import progressbar

PROCESSES_LENGHT = 10

class Process:
  def __init__(self, info, priority, duration, state=1, progressBar=None, pointer=None):
    self.info = info
    self.priority = priority
    self.duration = duration
    self.state = state
    self.pointer = pointer
    self.progressBar = progressBar

  def toString(self):
    print("Nome: " + str(self.info)+"\nDuração: "+str(self.duration)+"\nPrioridade: "+str(self.priority)+"\nEstado: "+str(self.state))

def up():
    # My terminal breaks if we don't flush after the escape-code
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

def down():
    # I could use '\x1b[1B' here, but newline is faster and easier
    sys.stdout.write('\n')
    sys.stdout.flush()

#1
processesCreated=[]
#2
processesReady=[]
#3
processesExecuting=[]
#4
processesBlocked=[]
#5
processesEnded=[]

for x in range(PROCESSES_LENGHT):
    p1 = Process("Processo "+str(x), random.randint(1,20), random.randint(1,10))
    # time.sleep(1)
    processesCreated.append(p1)

for process in processesCreated:
    newProgressBar = progressbar.ProgressBar(maxval=process.duration)
    process.progressBar = newProgressBar
    print(process.info+" | Duração: "+ str(process.duration)+ " Prioridade: "+str(process.priority))
    process.progressBar.start()
    process.state=2
    processesReady.append(process)
    down()
for i in range((PROCESSES_LENGHT*2) -1):
    up()
while True:
    allFinished=1
    for process in processesReady:
        processesExecuting.append(process)
        if(process.priority>=1 and process.priority<=7 ):
            quantum=2
        elif(process.priority>=8 and process.priority<=16):
            quantum=3
        else:
            quantum=4  

        for i in range(quantum):
            actualTime = process.progressBar.value
            if(actualTime+1 <= process.duration):
                process.progressBar.update(actualTime+1)
                time.sleep(0.5)
            else:
                # process.progressBar.finish()
                break
        down()
        down()
        if(process.progressBar.value!=process.duration):
            allFinished=0
        processesExecuting.pop()

    if(allFinished==1):
        break

    for i in range((PROCESSES_LENGHT*2)):
        up()