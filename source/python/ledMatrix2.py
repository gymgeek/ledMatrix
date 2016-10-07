import serial,json,time

class LedMatrix():
    serPort = None
    matrix =  [[[0,0,0] for x in range(15)] for x in range(8)] 
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
            self.serPort = serial.Serial(name, baudrate=9600)
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
            if i % 2:
                line.reverse()
                for pixel in line:
                    dataToSend.extend(pixel)
            else:
                for pixel in line:
                    dataToSend.extend(pixel)
        self.serPort.write(dataToSend)
    def clearMatrix(self):
        self.matrix =  [[[0,0,0] for x in range(15)] for x in range(8)]   

    def showText(self, intext, color=[55,55,55], delay=0.1,repeat=1):
        for __ in range(repeat):
            lines = [None for x in range(8)]
            text = ";"*15
            for letter in intext:
                text += letter + ";"
            text+=";"*2
            for letter in text:
                let = self.pismena[letter]
                
                for i in range(8):
                    letLine = let[i]
                    
                    for pixel in letLine:
                        
                        if lines[i] == None:                        
                            if pixel == 1:
                                lines[i] = [color]
                                
                            else:
                                lines[i] = [self.black]
                        else:
                            if pixel == 1:                          
                                lines[i].append(color)                            
                            else:
                                lines[i].append(self.black)
            
      
       
            for i in range(len(lines[i])):
                #print (i, end="")
                if len(lines[0]) >15:
                    ln = 15
                else:
                    ln = len(lines[0])-2
                for fr in range(ln):
                    if len(lines[0])>fr:                    
                        for lin in range(8):                       
                            self.matrix[lin][fr] = lines[7-lin][fr]
                self.sendToPanel()
                self.clearMatrix()
                for _ in range(1):
                    for ln in range(8):
                        if len(lines[ln])>1:
                            del lines[ln][0]
                time.sleep(delay)
            



    def setPanelColor(self,color):
        self.serPort.write(color*120)



    #tools
    def chunks(self,l, n):
        n = max(1, n)
        return [l[i:i + n] for i in range(0, len(l), n)]
            
        
        
        



ledMatrix = LedMatrix()

print( ledMatrix.openPort("COM15"))
