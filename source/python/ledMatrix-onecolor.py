import serial, json, time


class LedMatrix():
    serPort = None
    matrix = [[[0, 0, 0] for x in range(15)] for x in range(8)]
    pismena = {}
    black = [0, 0, 0]
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]

    count = 0  # debug

    # nacteni znaku
    with open('pismena.json') as f:
        pismena = (json.load(f))

    # otevreni portu
    def openPort(self, name):
        try:
            self.serPort = serial.Serial(name, baudrate=9600)
            time.sleep(5)
            return True
        except:
            return False

    def closePort(self):
        self.serPort.close()

    # odeslani matrixu na panel
    def sendToPanel(self, lines):


        rawData = ""
        for i in range(len(lines)):
            line = lines[i]

            if i % 2 == 0:
                line.reverse()
            for pixel in line:
                # print(pixel, end=": ")

                if pixel == [0, 0, 0]:
                    rawData += "0"
                    
                else:
                    rawData += "1"
                    
          

        dataToSend = [255]
        for i in rawData:
            if i == "1":
                dataToSend.append(49)
            else:
                dataToSend.append(48)
        dataToSend.append(10)
       
        
                           
        a = 0
        for i in dataToSend:
            a += 1
            self.serPort.write([i])
            if a % 60 == 0:
                time.sleep(0.01)
            


    def clearMatrix(self):
        self.matrix = [[[0, 0, 0] for x in range(15)] for x in range(8)]

    def showText(self, intext, repeat=1):
        for __ in range(repeat):
            color=[55, 55, 55]
            lines = [None for x in range(8)]
            # text = ";" * 15
            text = ""
            for letter in intext:
                text += letter + ";"
            # text += ";" * 2
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



            while len(lines[0]) < 15:
                for i in range(len(lines)):
                    lines[i] = [[0, 0, 0]] + lines[i]
                if len(lines[0]) < 15:
                    for i in range(len(lines)):
                        lines[i] = lines[i] + [[0, 0, 0]]

            if len(lines[0]) > 15:
                for i in range(len(lines)):
                    lines[i] = lines[i][0:15]


            self.sendToPanel(lines)

    def setPanelColor(self, color):
        self.serPort.write(color * 120)

    def stopwatch(self):
        start = time.time()
        while 1:
            sec = round(time.time() - start)
            mins = int(sec/60)
            sec = sec % 60
            self.showText(str(mins)+":"+("0"+str(sec))[-2:])
            while(time.time()-start)%60 < sec+1:
                pass


ledMatrix = LedMatrix()
print(ledMatrix.openPort("COM15"))
ledMatrix.showText("0:00")
