import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator
from Cost import Latency
latency = Latency()

#plotting 
plt.ion()
fig, ax = plt.subplots()

x_vals = []
y_vals = []
step = 0

# 1st Index is current choice, 2nd Index is a random timer dictating when they might update their route, 3rd Index is an threshold term suggesting how ready they are to change their choice (laziness)
Individuals = [[random.randint(0,1), random.random(), random.random()*0.1, 0] for x in range(0,100)]

#Hyperparameters
INERTIA = 1
ERROR1 = 0.1
ERROR2 = 0.01

#x() is the fraction choosing Route A
x = lambda:  sum((0==Individual[0]) for Individual in Individuals) / 100

def UpdateAlgorithm(Individual, Ca, Cb):

    error1 = (random.random()*2 - 1)*ERROR1
    error2 = (random.random()*2 - 1)*ERROR2

    Ca *= 1 + error1   #Scope of Ca, Cb is within the function
    Cb *= 1 + error2

    CurrentChoice = Individual[0]
    CurrentChoiceCost = Ca*(not CurrentChoice) + Cb*CurrentChoice
    OtherChoiceCost = Ca*(CurrentChoice) + Cb*(not CurrentChoice)
    
    Force = (CurrentChoiceCost - OtherChoiceCost) / CurrentChoiceCost
    
    Individual[3] += Force/INERTIA
    
    #The individual chooses the Route with least latency provided it is that much better than their current choice
    if Individual[3] >= Individual[2]:
        Individual[0] = int(Cb < Ca)
        Individual[3] = 0
    
    



while 1:
    Cb = 4 
    Ca = latency.RouteA_Cost(x()) 

    for Individual in Individuals:
        if Individual[1] <= 0:
            UpdateAlgorithm(Individual, Ca, Cb)
            Individual[1] = random.random()
        else:
            Individual[1] -= 0.1

    #Plotting   --AI--
    step += 1
    new_y = x()
    
    x_vals.append(step)
    y_vals.append(new_y)
    
    # Keep plot readable by only showing the last 50 points
    ax.clear()
    ax.plot(x_vals[-50:], y_vals[-50:], color="blue", marker="o")
    
    #Y-axis scaling between 0 and 1
    ax.set_ylim(0, 1)
    
    #Rolling Window
    ax.set_xlim(max(0, step - 50), max(50, step))
    ax.set_title("Live Signal Data")
    ax.set_xlabel("Time Step")
    ax.set_ylabel(f"Value avg(): {sum(y_vals[-50:])/len(y_vals[-50:]):.3f}")
    
    # Redraw frame and wait brief moment (0.05 seconds)
    plt.pause(0.05)
    