def CompressInfo(temperature, material, color, cycles, extraInfo):
    res = 90 * temperature + material * 30 + color * 10 + cycles
    #res = str(res) + extraInfo
    print("4: " + str(res))
    return res

def DecompressInfo(info):
    res = []
    res.append((((info % 90) % 30) % 10)) # cycles
    res.append((((info % 90) % 30) - res[0] )  / 10) #color
    res.append(((info % 90) - (res[1] *10) - res[0])  / 30) #material
    res.append( (info - (res[2] *30) - (res[1] *10) - res[0])  / 90) #temperature
    res.reverse()
    
    



    return res

box = CompressInfo(5,1,2,9,"hi")
print(DecompressInfo(box))