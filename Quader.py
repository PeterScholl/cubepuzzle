import json

class Quader:
    """ Klasse für Quader, die eine länge, breite, höhe besitzen und
    einen Offset von 0 """
    
    def __init__(self, lx,ly,lz, ox=0, oy=0, oz=0):
        self.lx = lx #Länge x-Richtung
        self.ly = ly
        self.lz = lz
        self.ox = ox #Offset x-Richtung
        self.oy = oy
        self.oz = oz
        
    def setoffset(self,ox,oy,oz):
        self.ox = ox #Offset x-Richtung
        self.oy = oy
        self.oz = oz
        
    def getMaxIn(self,richtung):
        if richtung=="x":
            return self.ox+self.lx
        if richtung=="y":
            return self.oy+self.ly
        if richtung=="z":
            return self.oz+self.lz
        return -1
    
    def setorientation(self,onr):
        l = [self.lx,self.ly,self.lz]
        l.sort()
        lw,mid,mx = l
        if (onr==0):
            self.lx,self.ly,self.lz = mx,mid,lw
        elif (onr==1):
            self.lx = lw
            self.ly = mx
            self.lz = mid
        elif (onr==2):
            self.lx = mid
            self.ly = lw
            self.lz = mx
        elif (onr==3):
            self.lx = mx
            self.ly = lw
            self.lz = mid
        elif (onr==4):
            self.lx = mid
            self.ly = mx
            self.lz = lw
        elif (onr==5):
            self.lx = lw
            self.ly = mid
            self.lz = mx
            
    def __str__(self):
        return f"lx,ly,lz: {self.lx},{self.ly},{self.lz} - ox,oy,oz: {self.ox},{self.oy},{self.oz}"
    
    def intersects(self,q,debug=False):
        #print(type(q), isinstance(q,Quader))
        if not isinstance(q,Quader): return False
        if not Quader.ueberlappendeStrecken(self.ox,self.ox+self.lx,q.ox,q.ox+q.lx):
            if debug: print(f"x-ueberlappt nicht",self,q)
            return False
        if not Quader.ueberlappendeStrecken(self.oy,self.oy+self.ly,q.oy,q.oy+q.ly):
            if debug: print(f"y-ueberlappt nicht",self,q)
            return False
        if not Quader.ueberlappendeStrecken(self.oz,self.oz+self.lz,q.oz,q.oz+q.lz):
            if debug: print(f"z-ueberlappt nicht",self,q)
            return False
        return True
    
    @staticmethod
    def ueberlappendeStrecken(a1,a2,b1,b2):
        """ a1<a2 bestimmen die Strecke 1 und b1<b2 bestimmen Strecke 2 """
        if b1 <= a1 and a1 < b2: return True
        if b1 < a2 and a2 <= b2: return True
        if a1 <= b1 and b1 < a2: return True
        if a1 < b2 and b2 <= a2: return True
        return False
        
def check_validity(orientation, debug = True):
    global qList
    qList = []
    if (len(orientation)!= 27):
        return False
    for i in range(27):
        if orientation[i]==-1: break
        n = Quader(9,10,11)
        n.setorientation(orientation[i])
        qList.append(n)
        if (i==1): #zweiter Quader ca. (10,0,0)
            n.ox = qList[0].lx
            if qList[i].getMaxIn("x") < 19 or qList[i].getMaxIn("x") > 21: return False
        elif (i==2): #dritter Quader ca. (20,0,0)
            n.ox = qList[1].ox + qList[1].lx
            if n.ox+n.lx != 30:
                if (debug): print("dritter Quader ausserhalb")
                return False
        elif (i==3): #vierter Quader ca. (0,10,0)
            n.oy = qList[0].ly
            #Prüfen ob vorstehende Ecke in die Mitte bei Quader 0
            if qList[1].ly < qList[0].ly and n.lx < qList[0].lx: return False
            if qList[i].getMaxIn("y") < 19 or qList[i].getMaxIn("y") > 21: return False
        elif (i==4): #fünfter Quader Mitte im Boden
            n.oy = qList[1].ly
            n.ox = qList[3].lx
            #Prüfen ob vorstehende Ecke von Quader 1
            if qList[2].ly < qList[1].ly and n.lx+n.ox < qList[1].lx+qList[1].ox: return False
            if qList[i].getMaxIn("x") < 19 or qList[i].getMaxIn("x") > 21: return False
            if qList[i].getMaxIn("y") < 19 or qList[i].getMaxIn("y") > 21: return False
        elif (i==5): #sechster Quader
            n.oy = qList[2].ly
            n.ox = qList[4].ox+qList[4].lx
            if n.ox+n.lx != 30:
                if (debug): print("sechster Quader ausserhalb")
                return False
            if qList[i].getMaxIn("y") < 19 or qList[i].getMaxIn("y") > 21: return False
        elif (i==6): #siebter Quader ca. (0,20,0)
            n.oy = qList[3].getMaxIn("y")
            if n.oy+n.ly != 30:
                if (debug): print("Quader 6 steht über", n.oy+n.ly)
                return False
            #Prüfen ob vorstehende Ecke in die Mitte bei Quader 3
            if qList[4].getMaxIn("y") < qList[3].getMaxIn("y") and n.lx < qList[3].lx:
                if (debug): print("vorstehende Ecke bei Quader 3")
                return False
        elif (i==7): #achter Quader ca (10,20,0)
            n.oy = qList[4].getMaxIn("y")
            n.ox = qList[6].lx
            if n.oy+n.ly != 30: return False #Prüfung ob Überstand
            #Prüfen ob vorstehende Ecke von Quader 4
            if qList[5].getMaxIn("y") < qList[4].getMaxIn("y") and n.lx+n.ox < qList[4].getMaxIn("x"):
                if (debug): print("Überstehende Ecke bei Quader 4 (mitte)")
                return False
            if qList[i].getMaxIn("x") < 19 or qList[i].getMaxIn("x") > 21: return False
        elif (i==8): #neunterQuader
            n.oy = qList[5].getMaxIn("y")
            n.ox = qList[7].getMaxIn("x")
            if n.ox+n.lx != 30 or n.oy+n.ly !=30:
                if (debug): print("neunter Quader ausserhalb")
                return False
        elif (i==9): #neunter Quader ca. (0,0,10)
            #Position festlegen
            n.oz = qList[0].getMaxIn("z")
            # Kollisionen prüfen
            if n.intersects(qList[1]) or n.intersects(qList[3]) or n.intersects(qList[4]):
                if (debug): print("Quader 9 überlappt mit 1,3, oder 4")
                return False
            if qList[i].getMaxIn("z") < 19 or qList[i].getMaxIn("z") > 21: return False
        elif (i==10): #zehnter Quader ca (10,20,0)
            #Position festlegen
            n.oz = qList[1].getMaxIn("z")
            n.ox = qList[9].getMaxIn("x")
            # Kollisionen prüfen
            if n.intersects(qList[0]) or n.intersects(qList[3]) or n.intersects(qList[4]) or n.intersects(qList[5]) or n.intersects(qList[2]):
                if (debug): print("Quader 10 überlappt mit 0,2,3,4 oder 5")
                return False
            if qList[i].getMaxIn("x") < 19 or qList[i].getMaxIn("x") > 21: return False
            if qList[i].getMaxIn("z") < 19 or qList[i].getMaxIn("z") > 21: return False
        elif (i==11): #elfter Quader
            #Position festlegen
            n.oz = qList[2].getMaxIn("z")
            n.ox = qList[10].getMaxIn("x")
            # Kollisionen prüfen
            if n.intersects(qList[1]) or n.intersects(qList[4]) or n.intersects(qList[5]):
                if (debug): print("Quader 11 überlappt mit 1,4 oder 5")
                return False
            if n.ox+n.lx != 30:
                if (debug): print("elfter Quader ausserhalb")
                return False
            if qList[i].getMaxIn("z") < 19 or qList[i].getMaxIn("z") > 21: return False
        elif (i==12): #zwölfter Quader ca. (0,10,10)
            #Position festlegen
            n.oz = qList[3].getMaxIn("z")
            n.oy = qList[9].getMaxIn("y")
            # Kollisionen prüfen
            if n.intersects(qList[0]) or n.intersects(qList[1]) or n.intersects(qList[4]) or n.intersects(qList[6]) or n.intersects(qList[7]) or n.intersects(qList[10]):
                if (debug): print("Quader 12 überlappt mit einem Nachbarn")
                return False
            if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
        elif (i==13): #dreizehnter Quader ca (10,10,10)
            #Position festlegen
            n.oz = qList[4].getMaxIn("z")
            n.oy = qList[10].getMaxIn("y")
            n.ox = qList[12].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [0,1,2,3,5,6,7,8,9,11]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("x") < 19 or n.getMaxIn("x") > 21: return False
            if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
        elif (i==14): #vierzehnter Quader
            #Position festlegen
            n.oz = qList[5].getMaxIn("z")
            n.oy = qList[11].getMaxIn("y")
            n.ox = qList[13].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [1,2,4,7,8,10]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.ox+n.lx != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==15): #fünfzehnter Quader ca. (0,20,10)
            #Position festlegen
            n.oz = qList[6].getMaxIn("z")
            n.oy = qList[12].getMaxIn("y")
            # Kollisionen prüfen
            for nr in [3,4,7,13]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.oy+n.ly != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==16): #sechzenter Quader ca (10,20,10)
            #Position festlegen
            n.oz = qList[7].getMaxIn("z")
            n.oy = qList[13].getMaxIn("y")
            n.ox = qList[15].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [3,4,5,6,8,12,14]:
                if n.intersects(qList[nr]):
                    if(debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("x") < 19 or n.getMaxIn("x") > 21:
                if(debug): print(f"{i} Oversize x")
                return False
            if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: 
                if(debug): print(f"{i} Oversize z")
                return False
            if n.oy+n.ly != 30:
                if(debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==17): # Quader
            #Position festlegen
            n.oz = qList[8].getMaxIn("z")
            n.oy = qList[14].getMaxIn("y")
            n.ox = qList[16].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [4,5,7,13]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            #if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.ox+n.lx != 30 or n.oy+n.ly != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==18): #Quader ca. (0,0,20)
            #Position festlegen
            n.oz = qList[9].getMaxIn("z")
            #n.oy = qList[12].getMaxIn("y")
            # Kollisionen prüfen
            for nr in [10,12,13]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            #if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.oz+n.lz != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==19): #Quader ca (10,0,20)
            #Position festlegen
            n.oz = qList[10].getMaxIn("z")
            #n.oy = qList[13].getMaxIn("y")
            n.ox = qList[18].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [9,11,12,13,14]:
                if n.intersects(qList[nr]):
                    if(debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("x") < 19 or n.getMaxIn("x") > 21:
                if(debug): print(f"{i} Oversize x")
                return False
            if n.oz+n.lz != 30:
                if(debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==20): # Quader
            #Position festlegen
            n.oz = qList[11].getMaxIn("z")
            #n.oy = qList[14].getMaxIn("y")
            n.ox = qList[19].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [10,13,14]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            #if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            #if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.ox+n.lx != 30 or n.oz+n.lz != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==21): #Quader ca. (0,10,20)
            #Position festlegen
            n.oz = qList[12].getMaxIn("z")
            n.oy = qList[18].getMaxIn("y")
            # Kollisionen prüfen
            for nr in [9,10,13,15,16,19]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            if n.oz+n.lz != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==22): #Quader ca (10,10,20)
            #Position festlegen
            n.oz = qList[13].getMaxIn("z")
            n.oy = qList[19].getMaxIn("y")
            n.ox = qList[21].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [9,10,11,12,14,15,16,17,18,20]:
                if n.intersects(qList[nr]):
                    if(debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("x") < 19 or n.getMaxIn("x") > 21:
                if(debug): print(f"{i} Oversize x")
                return False
            if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21:
                if(debug): print(f"{i} Oversize x")
                return False
            if n.oz+n.lz != 30:
                if(debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==23): # Quader (20,10,20)
            #Position festlegen
            n.oz = qList[14].getMaxIn("z")
            n.oy = qList[20].getMaxIn("y")
            n.ox = qList[22].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [10,11,13,19]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            #if n.getMaxIn("z") < 19 or n.getMaxIn("z") > 21: return False
            if n.ox+n.lx != 30 or n.oz+n.lz != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==24): #Quader ca. (0,20,20)
            #Position festlegen
            n.oz = qList[15].getMaxIn("z")
            n.oy = qList[21].getMaxIn("y")
            # Kollisionen prüfen
            for nr in [12,13,16,22]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            #if n.getMaxIn("y") < 19 or n.getMaxIn("y") > 21: return False
            if n.oz+n.lz != 30 or n.oy+n.ly != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==25): #Quader ca (10,20,20)
            #Position festlegen
            n.oz = qList[16].getMaxIn("z")
            n.oy = qList[22].getMaxIn("y")
            n.ox = qList[24].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [12,13,14,15,17,21,23]:
                if n.intersects(qList[nr]):
                    if(debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.getMaxIn("x") < 19 or n.getMaxIn("x") > 21:
                if(debug): print(f"{i} Oversize x")
                return False
            if n.oz+n.lz != 30 or n.oy+n.ly != 30:
                if(debug): print(f"{i}ter Quader ausserhalb")
                return False
        elif (i==26): # Quader (20,20,20)
            #Position festlegen
            n.oz = qList[17].getMaxIn("z")
            n.oy = qList[23].getMaxIn("y")
            n.ox = qList[25].getMaxIn("x")
            # Kollisionen prüfen
            for nr in [13,14,16,22]:
                if n.intersects(qList[nr]):
                    if (debug): print(f"Quader {i} überlappt mit Quader {nr}")
                    return False
            if n.ox+n.lx != 30 or n.oy+n.ly != 30 or n.oz+n.lz != 30:
                if (debug): print(f"{i}ter Quader ausserhalb")
                return False
            
    return True

def QuaderSearch():
    aktpos=0
    orientation = [-1 for _ in range(27)]
    count = 0
    while aktpos >= 0 and aktpos < 27:
        count+=1
        if (count>10000):
            print(orientation[0:9], check_validity(orientation,debug=True))
            count=0
        if orientation[aktpos] < 6:
            orientation[aktpos]+=1
            if (check_validity(orientation, debug=False)):
                aktpos+=1
                if (aktpos<27): orientation[aktpos]=-1 #eigentlich nicht nötig
        else:
            orientation[aktpos]=-1
            aktpos -=1
    if (aktpos>0): print("QuaderSearchSuccess", orientation)

def QuaderSearchGen():
    aktpos=0
    orientation = [-1 for _ in range(27)]
    while aktpos >= 0 and aktpos < 27:
        if orientation[aktpos] < 6:
            orientation[aktpos]+=1
            if (check_validity(orientation, debug=False)):
                aktpos+=1
                if (aktpos>=27):
                    yield orientation
                    aktpos-=1
                else:
                    orientation[aktpos]=-1 #eigentlich nicht nötig
        else:
            orientation[aktpos]=-1
            aktpos -=1
    
def test():
    q1 = Quader(3,2,1,1,1,1)
    q2 = Quader(2,3,1,2,2,2)
    print("Quader q1",q1)
    print("Quader q2",q2)
    print("Die Quader überlappen", q1.intersects(q2, debug=True))
    for i in range(6):
        q1.setorientation(i)
        print(f"Orientation {i}: {q1}");

def generateCubes(qList):
    colors = ["red","blue","#43d92e","#d9d968","#416e68","#f1ce68","#2b2be1","#ebd836","#3ed836","#de1be9","#1bee13","#1b10f0","#fe10f0","#08f8f6","#04ac04","#ebac04","#08f8e6"]
    cubes = []
    for i in qList:
        aktcol = colors.pop(0)
        q={}
        q["position"] = [i.ox,i.oy,i.oz]
        q["size"] = [i.lx,i.ly,i.lz]
        q["color"] = aktcol
        q["visible"] = "True"
        cubes.append(q)
        colors.append(aktcol)
    return cubes

def saveCubes(cubes, filename="cubes.json"):
    with open(filename, "w") as file:
                json.dump(list(cubes), file, indent=4)  # `cubes` in JSON speichern

def test_check_v():
    global qList
    orientation = [1,0,2,0,1,4,2,3,0, *(-1 for _ in range(18))]
    orientation = [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    print(orientation, "is valid:", check_validity(orientation) )
    for q in qList:
        print(q)
    print(len(qList))

if __name__=="__main__":
    #test()
    test_check_v()
    