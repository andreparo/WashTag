
def DevideString(inputStr):
    lastHashstag = -1
    res = []
    for i in range(len(inputStr)):
        if(inputStr[i] == "#"):
            res.append(inputStr[lastHashstag+1:i])
            
            #testprint
            print(inputStr[lastHashstag+1:i])
            lastHashstag = i

    return res



def CompressInfo(temperature, material, color, cycles, extraInfo):
    res = 90 * temperature + material * 30 + color * 10 + cycles
    #res = str(res) + extraInfo
    #print("4: " + str(res))
    return res

def DecompressInfo(info):
    #info is array in this format ["123ADIDAS", "654NIKE"]
    arrayOfRes = []
    for i in info:
        infoInt = int(i[0:3])

        
        res = []
        res.append((((infoInt % 90) % 30) % 10)) # cycles
        res.append((((infoInt % 90) % 30) - res[0] )  / 10) #color
        res.append(((infoInt % 90) - (res[1] *10) - res[0])  / 30) #material
        res.append( (infoInt - (res[2] *30) - (res[1] *10) - res[0])  / 90) #temperature
        res.reverse()
        res.append("")
        res.append(str(i[3:len(i)]))
        arrayOfRes.append(res)




    return arrayOfRes


testString = "123ADIDAS#456NIKE#"
print(DevideString(testString))

#box = CompressInfo(5,1,2,9,"hi")
print(DecompressInfo(DevideString(testString)))