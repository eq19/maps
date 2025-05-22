import os.path

"""
Returns list: [size,color from last element]
"""
def fileLen(filepath):
    with open(filepath) as fp:  
        line = fp.readline()
        cnt = 0
        while line:
            color = int(line)
            cnt += 1
            line = fp.readline()
    return [cnt, color]
    
"""
Returns: color
"""
def fileLineColor(searched_line,filepath):
    with open(filepath) as fp:  
        line = fp.readline()
        cnt = 0
        while cnt <= searched_line:
            color = int(line)
            cnt += 1
            line = fp.readline()
        
        if cnt != searched_line+1:
            print ("ERROR! Line doesn't exist")
            return -1
    return color
    
"""
Returns: integer value of color of last line in previous file
"""
def getFinalizedColor(datadir, filepath):
    fullpath = datadir + '/' + filepath[0] + '/' + filepath[1:3] + '/' + filepath[3:5] + '/' + filepath[5:7] + '/' + filepath[7:]
    if not os.path.isfile(fullpath):
	    return None
    with open(fullpath) as fp:
	    return fp.readlines()[-1]
