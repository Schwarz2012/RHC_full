def collect(self, *args):
        geomunits = self.geomspinner.text 
        if geomunits == 'm':
            correct = 1
        elif geomunits == 'cm':
            correct = 0.01
        elif geomunits == 'mm':
            correct = 0.001
        tempunits = self.tempspinner.text
        if tempunits != 'K':
            tempcorrect = 0
        elif tempunits == 'K':
            tempcorrect = 273.15        
        #Collect data
        self.result = {}
        self.result['RG'] = [float(self.Room['RL'].text)*correct, float(self.Room['RW'].text)*correct, float(self.Room['RH'].text)*correct]
        #Walls
        Uwall = []
        EPSwall = []
        Texwall = []
        #Walls RS
        EPSwallRS = [[],[],[],[]]
        TinwallRS = [[],[],[],[]]
        wallRScoord = [[],[],[],[]]
        wallRScoord_list = []
        #Walls OP 
        wallOpcoord = [[], [], [], []]
        EPSwallOp = [[], [], [], []]        
        UwallOp = [[], [], [], []]
        wallOpcoord_list = []
        #Floor
        floorRScoord = []
        floorRScoord_list = []
        EPSfloorRS = []
        TfloorRS = []
        #Ceiling
        ceilingRScoord = []
        ceilingRScoord_list = []
        EPSceilingRS = []
        TceilingRS = []

        for i in range(1,5,1):
            Uwall.append(float(self.WallParInput['U' + str(i)].text))
            EPSwall.append(float(self.WallParInput['Eps' + str(i)].text))
            Texwall.append(float(self.WallParInput['Tex' + str(i)].text) - tempcorrect)
            for j in range(len(self.wallRSdata[i-1])):
                wallRScoord_list.clear()
                EPSwallRS[i-1].append(float(self.wallRSpar[self.wallRSdata[i-1][j] + 'Eps'].text))
                TinwallRS[i-1].append(float(self.wallRSpar[self.wallRSdata[i-1][j] + 'TRS'].text) - tempcorrect)
                wallRScoord_list.append(float(self.wallRScoord[self.wallRSdata[i-1][j] + 'x_corn'].text)*correct)
                wallRScoord_list.append(float(self.wallRScoord[self.wallRSdata[i-1][j] + 'Widht'].text)*correct)
                wallRScoord_list.append(float(self.wallRScoord[self.wallRSdata[i-1][j] + 'y_corn'].text)*correct)
                wallRScoord_list.append(float(self.wallRScoord[self.wallRSdata[i-1][j] + 'Hight'].text)*correct)
                wallRScoord[i-1].append(wallRScoord_list)
            for k in range(len(self.wallOpdata[i-1])):
                wallOpcoord_list.clear()
                EPSwallOp[i-1].append(float(self.wallOppar[self.wallOpdata[i-1][k] + 'Eps'].text))
                UwallOp[i-1].append(float(self.wallOppar[self.wallOpdata[i-1][k] + 'U'].text))
                wallOpcoord_list.append(float(self.wallOpcoord[self.wallOpdata[i-1][k] + 'x_corn'].text)*correct)
                wallOpcoord_list.append(float(self.wallOpcoord[self.wallOpdata[i-1][k] + 'Widht'].text)*correct)
                wallOpcoord_list.append(float(self.wallOpcoord[self.wallOpdata[i-1][k] + 'y_corn'].text)*correct)
                wallOpcoord_list.append(float(self.wallOpcoord[self.wallOpdata[i-1][k] + 'Hight'].text)*correct)
                wallOpcoord[i-1].append(wallOpcoord_list)
        for i in range(len(self.floorRSdata)):
            floorRScoord_list.clear()
            EPSfloorRS.append(float(self.floorRSpar['FloorRS' + self.floorRSdata[i] + 'Eps'].text))
            TfloorRS.append(float(self.floorRSpar['FloorRS' + self.floorRSdata[i] + 'TRS'].text) - tempcorrect)
            floorRScoord_list.append(float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'x_corn'].text)*correct)
            floorRScoord_list.append(float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'Widht'].text)*correct)
            floorRScoord_list.append(float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'y_corn'].text)*correct)
            floorRScoord_list.append(float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'Length'].text)*correct)
            floorRScoord.append(floorRScoord_list)
        for i in range(len(self.ceilingRSdata)):
            ceilingRScoord_list.clear()
            EPSceilingRS.append(float(self.ceilingRSpar['CeilingRS' + self.ceilingRSdata[i] + 'Eps'].text))
            TceilingRS.append(float(self.ceilingRSpar['CeilingRS' + self.ceilingRSdata[i] + 'TRS'].text) - tempcorrect)
            ceilingRScoord_list.append(float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'x_corn'].text)*correct)
            ceilingRScoord_list.append(float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'Widht'].text)*correct)
            ceilingRScoord_list.append(float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'y_corn'].text)*correct)
            ceilingRScoord_list.append(float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'Length'].text)*correct)
            ceilingRScoord.append(ceilingRScoord_list)

        self.result['Uwall'] = Uwall
        self.result['EPSwall'] = EPSwall
        self.result['Texwall'] = Texwall

        self.result['EPSwallRS'] = EPSwallRS
        self.result['TinwallRS'] = TinwallRS
        self.result['wallRScoord'] = wallRScoord

        self.result['EPSwallOp'] = EPSwallOp
        self.result['TexwallOp'] = Texwall
        self.result['UwallOp'] = UwallOp
        self.result['wallOpcoord'] = wallOpcoord
      
        self.result['Ufloor'] = float(self.FloorParInput['U'].text)
        self.result['EPSfloor'] = float(self.FloorParInput['Eps'].text)
        self.result['Texfloor'] = float(self.FloorParInput['Tex'].text) - tempcorrect

        self.result['EPSfloorRS'] = EPSfloorRS
        self.result['TfloorRS'] = TfloorRS
        self.result['floorRScoord'] = floorRScoord

        self.result['Uceiling'] = float(self.CeilingParInput['U'].text)
        self.result['EPSceiling'] = float(self.CeilingParInput['Eps'].text)
        self.result['Texceiling'] = float(self.CeilingParInput['Tex'].text) - tempcorrect

        self.result['EPSceilingRS'] = EPSceilingRS
        self.result['TceilingRS'] = TceilingRS
        self.result['ceilingRScoord'] = ceilingRScoord
        return(self.result)