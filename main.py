import sys
import time
import random
import progressbar

PROCESSES_LENGHT = 15 # Numero processos
QUANTUM_DURATION = 0.5 # Duração do quantum em segundos
INTERRUPTION_CHANCE = 5 # 1=100%, 2=50%, 3=33%, 4=25%, 5=20% ...
PROCESS_MAX_DURATION = 10

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

# Sobe no terminal
def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

# Desce no terminal
def down():
    # I could use '\x1b[1B' here, but newline is faster and easier
    sys.stdout.write('\n')
    sys.stdout.flush()

#1
processesCreated=[]
#2
processesReady=[]
#3
# processesExecuting=[]
#4
# processesBlocked=[]
#5
# processesEnded=[]

# Cria processos
for x in range(PROCESSES_LENGHT):
    p1 = Process("Processo "+str(x), random.randint(1,20), random.randint(1,PROCESS_MAX_DURATION))
    # time.sleep(1)
    processesCreated.append(p1)

# Cria barra de progresso
for process in processesCreated:
    newProgressBar = progressbar.ProgressBar(maxval=process.duration)
    process.progressBar = newProgressBar
    print(process.info+" | Duração: "+ str(process.duration)+ " Prioridade: "+str(process.priority))
    process.progressBar.start()
    process.state=2
    processesReady.append(process)
    down()

# Volta para cima no terminal
for i in range((PROCESSES_LENGHT*2)-1):
    up()

# Feedback visual para processo terminado
def printEnded(process,first):
    up()
    up()
    print("P"+process.info+" | Duração: "+ str(process.duration)+ " Prioridade: "+str(process.priority)+" **ENDED**")
    process.progressBar.update(process.progressBar.value)

# Feedback visual para processo bloqueado
def printBlocked(process,first):
    if(first==False):
        up()
    up()
    print("P"+process.info+" | Duração: "+ str(process.duration)+ " Prioridade: "+str(process.priority)+" **BLOCKED**")
    process.progressBar.update(process.progressBar.value)

# Feedback visual para processo normal/ready
def printNormal(process):
    up()
    print(process.info+" | Duração: "+ str(process.duration)+ " Prioridade: "+str(process.priority)+"              ")
    process.progressBar.update(process.progressBar.value)

# Função simulando chamada de sistema, bloqueando o processo
def systemCallInterruption(process,first):
    if(random.randint(1,5)==1 and process.state!=5 and process.state!=4):
        process.state=4
        process.priority = process.priority+7
        if(process.priority>=20): process.priority=20
        printBlocked(process,first)
        down()
        down()
        return True
    return False

# Execução de processos (CPU)
def steps(process,first):

    #Quantum
    if(process.priority>=1 and process.priority<=7 ):
        quantum=2
    elif(process.priority>=8 and process.priority<=16):
        quantum=3
    else:
        quantum=4  
   
    if(process.state != 5):
        printNormal(process)

    notEnded=1
    for i in range(quantum):
        actualTime = process.progressBar.value
        #Possivel interrupção por chamada de sistema
        if(systemCallInterruption(process,first)) : return

        if(actualTime+1 <= process.duration):
            process.progressBar.update(actualTime+1)
            time.sleep(QUANTUM_DURATION)
            if(process.progressBar.value == process.duration):
                process.state=5
                printEnded(process,first)
                notEnded=0
                break
            
        else:
            process.state=5
            notEnded=0
            break
    
    #Interrupção por preempção
    if(notEnded==1):
        process.priority = process.priority-7
        if(process.priority<=0): process.priority=1

    down()
    down()

while True:
    allFinished=1
    first=True
    for process in processesReady:
        steps(process,first)
        if(process.progressBar.value!=process.duration):
            allFinished=0
        first=False

    # Chance de criar um novo processo
    # if(random.randint(1,1)==1):
    #     up()
    #     p1 = Process("\nProcesso "+str(PROCESSES_LENGHT), 20, random.randint(1,10), 2)
    #     PROCESSES_LENGHT = PROCESSES_LENGHT + 1
    #     newProgressBar = progressbar.ProgressBar(maxval=p1.duration)
    #     p1.progressBar = newProgressBar
    #     p1.progressBar.start()
    #     processesReady.append(p1)
    #     steps(p1,False)

    if(allFinished==1):
        break

    # Volta para a parte de cima do terminal
    for i in range(PROCESSES_LENGHT*2):
        up()