import csv
fileR = open("LetterVectors.csv", "r")
fileW = open("LetterVectorsNormalised.csv", "w")

reader = csv.reader(fileR)
writer = csv.writer(fileW)

def normiliser(vectorAxis):
    normalised = []
    axrange = max(vectorAxis)-min(vectorAxis)
    for i in range(0, len(vectorAxis)):
        normalised.append((vectorAxis[i]-min(vectorAxis))/axrange)
    return normalised

for row in reader:
    char = row[0]
    vector = []
    for i in range(1, len(row)):
        vector.append(float(row[i]))
    
    vectorX, vectorY, vectorZ = [], [], []
    for i in range(len(vector)//3):
        vectorX.append(vector[0+(i*3)])
        vectorY.append(vector[1+(i*3)])
        vectorZ.append(vector[2+(i*3)])
    
    vector = [char]
    vector.extend(normiliser(vectorX))
    vector.extend(normiliser(vectorY))
    vector.extend(normiliser(vectorZ))
    
    writer.writerow(vector)

        