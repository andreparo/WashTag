import time

def calculateFlags(toAdd, prog):
    for f in range(len(toAdd)):
            flag = 0
            if toAdd[f][0] != prog[0]:
                flag += abs((toAdd[f][0] - prog[0])*20)
            if toAdd[f][1] != prog[1]:
                flag += 40
            if toAdd[f][2] != prog[2]:
                if toAdd[f][2] != "w" and prog[2] == "w":
                    flag += 40
                if toAdd[f][2] == "w" and prog[2] != "w":
                    flag += 40
            if toAdd[f][3] != prog[3]:
                flag += abs((toAdd[f][3] - prog[3])*10)
            toAdd[f].append(flag)
    return toAdd


def recalculateFlags(array, program):
    for i in range (len(array)):
        array[i].pop(4)

    #*testing
    print("reset time")
    print(array)
    
    

    array = calculateFlags(array, program)
    return array




count = 0
cycleEvery = 3
input = []   #input array of clothes
currentProgram = [] # current Program
general = [] #array of all elements apperared until now
#*
in1 = [0,"c", "w", 0]
in2 = [2,"c", "b", 3]
progT = [2,"c", "b", 3]

input.append(in1)
input.append(in2)
currentProgram = progT   
#*
while(1==1):
    count += 1

    #! RESET INPUT
    #! RESET CURRENT PROGRAM

    toAdd = []
    #check if input as new elements and append them to general
    if(len(general) == 0):  #when general is empty
        toAdd = input
        
        general = calculateFlags(toAdd, currentProgram)
    else:
        time.sleep(cycleEvery)

        #fill toAdd with elements that are not already present
        for i in range(len(input)):
            equal = True
            present = False
            for a in range(len(general)):
                
                
                if(input[i][0] == general[a][0]):
                    equal = True
                else:
                    equal = False
                if(equal and input[i][1] == general[a][1]):
                    equal = True
                else:
                    equal = False
                if(equal and input[i][2] == general[a][2]):
                    equal = True
                else:
                    equal = False
                if(equal and input[i][3] == general[a][3]):
                    equal = True
                    present = True
                else:
                    equal = False

                if(present):
                   break
            
            if(not present):
                #testprint
                #print("added to toAdd: ")
                #print(input[i])
                toAdd.append(input[i])
        print("toAdd created: ")
        print(toAdd)

        #check for flags in toAdd
    
        #add "suitable for wash" flag
        toAdd = calculateFlags(toAdd, currentProgram)

        #append toAdd to general
        if(len(toAdd) != 0):
            #testprint
            print("toAdd after flag of size: " + str(len(toAdd)))
            print(toAdd)
            for t in range(len(toAdd)):
                general.append(toAdd[t])

            
        #sort based on ">flag first"
        #selection sorting for flags



        #print("testing gen")
        #print(general)

        

        general.sort(key=lambda x:x[4])
        general.reverse()
        #print("sorted general")
        #print(general)
        #print("---")
            



        #* TESTING
        #print("testing updated")
        in4 = [1,"s", "b", 2]
        in5 = [4,"c", "w", 7]
        in3 = [4,"c", "c", 7]
        progb = [2,"c", "c", 5]
        input = []
        
        input.append(in4)
        input.append(in5)
        input.append(in3)

        #*
        if(count == 5):
            currentProgram = progb
            general = recalculateFlags(general, currentProgram)


    #testprint
    print("End of cycle: " + str(count))
    print(currentProgram)
    print(general)
    print("-------------------------------------------------")


    