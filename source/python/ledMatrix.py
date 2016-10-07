import serial,json,time

class LedMatrix():
    serPort = None
    matrix =  [[[0,0,0] for x in range(15*3)] for x in range(8)] 
    pismena = {}
    black = [0,0,0]
    red = [255,0,0]
    green = [0,255,0]
    blue = [0,0,255]

    count = 0 #debug
    
    #nacteni znaku
    with open('pismena.json') as f:
        pismena = (json.load(f))
    #otevreni portu
    def openPort(self,name):
        try:
            self.serPort = serial.Serial(name)
            return True
        except:
            return False
    def closePort(self):
        self.serPort.close()

    #odeslani matrixu na panel
    def sendToPanel(self):
        dataToSend = []
        for i in range(len(self.matrix)):
            line = self.matrix[i]            
            
            if not i % 2:
                linerev = self.chunks(line,3)
                linerev.reverse()
                line=[]
                for lnr in linerev:
                    line.append(lnr)
            for lin in line:
                if not type(lin) == int:                    
                    for li in lin:
                        dataToSend.append(li)
                else:
                    dataToSend.append(lin)
        
        #if len(dataToSend) <= 360:
        self.serPort.write(dataToSend)
    def clearMatrix(self):
        self.matrix =  [[0 for x in range(15*3)] for x in range(8)]   

    def showText(self, intext, color=[50,0,50], delay=0.1):
        lines = [None for x in range(8)]
        text = ";"*15
        for letter in intext:
            text += letter + ";"
        text+=";"*16
        for letter in text:
            let = self.pismena[letter]
            
            for i in range(8):
                letLine = let[i]
                
                for pixel in letLine:
                    
                    if lines[i] == None:                        
                        if pixel == 1:
                            lines[i] = [color[0]]
                            lines[i].append(color[1])
                            lines[i].append(color[2])
                        else:
                            lines[i] = [self.black[0]]
                            lines[i].append(self.black[1])
                            lines[i].append(self.black[2])                            
                            
                    else:
                        if pixel == 1:                          
                            lines[i].append(color[0])
                            lines[i].append(color[1])
                            lines[i].append(color[2])
                        else:
                            lines[i].append(self.black[0])
                            lines[i].append(self.black[1])
                            lines[i].append(self.black[2])
        
        #return lines
        #for i in range(8):
        #    lines[i].reverse()
        print (len(lines[i]))
        for i in range(int(len(lines[i])/3.0)):
            print(i)
            if len(lines[0]) >15*3:
                ln = 15*3
            else:
                ln = len(lines[0])
            for fr in range(ln):
                if len(lines[0])>44:
                    for ln in range(8):
                        self.matrix[ln][fr] = lines[7-ln][44-fr]
            #print(lines)
            self.sendToPanel()
            #self.clearMatrix()
            for _ in range(3):
                for ln in range(8):
                    if len(lines[ln])>1:
                        del lines[ln][0]
            time.sleep(delay)
            







    #tools
    def chunks(self,l, n):
        n = max(1, n)
        return [l[i:i + n] for i in range(0, len(l), n)]
            
        
        
        



ledMatrix = LedMatrix()

ledMatrix.openPort("COM3")
