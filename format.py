
def mAgCardName(name):
    if(name == "VS"):
        return "VISA "
    elif(name == "MC"):
        return "MCRD "
    elif(name == "DS"):
        return "DISC "
    elif(name == "AX"):
        return "AEXP "
    elif(name == "VF"):
        return "VOYG "
    else:
        return "UNKNO"

#lR is what part the padding gets added to. Left is before the input string and right is after the input string.
def padAdd(lR, fill, length, input):
    output = str(input)
    padding = ""
    
    for __ in range(length - len(str(input))):
        padding = fill + padding
    if lR == "left":
        output = padding + output
    elif lR == "right":
        output = output + padding 
    return str(output)

#lR is justification. Left justified or right justified for the length cut.
def cutLength(lR, length, input):
    output = str(input)
    if length < len(input):
        if lR == "left":
            output = output[0:length]
        else:
            output = output[(len(output)-length):(len(output))]
    return str(output)


def decimalFormat(sigFig, input):
    output = input.split(".")
    temp = ""
    if len(output) == 1:
        for __ in range(sigFig):
            temp = temp + "0"
        output.append(temp)
    output[1] = padAdd("right", "0", sigFig, str(output[1]))
    return (str(output[0]) + str(output[1]))

def decimalPad(sigFig, input):
    output = input.split(".")
    temp = ""
    if len(output) == 1:
        for __ in range(sigFig):
            temp = temp + "0"
        output.append(temp)
    else:
        if (len(output[1])>sigFig):
            output[1] = output[1][0:sigFig]
    return str(output[0]) + "." + padAdd("right", "0", sigFig, str(output[1]))