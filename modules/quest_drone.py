import quest
import Vector
import VS
import unit
import vsrandom

drone=VS.Unit()
derelict=VS.Unit()
def generateBase ():
    global derelict
    derelict=VS.launch("Base","derelict","neutral","unit","sitting_duck",1,1,(0,-17000,-15000),'')

class quest_drone (quest.quest):
    def setup(self):
        self.sysfile = VS.getSystemFile()
        self.stage=0
        self.lastdist=10000
        self.jumping=0
        self.savedplaya=VS.getPlayer()
        print ("initiating")
    def __init__ (self):
        self.setup()
    def launchNewDrone (self):
        global drone
        playa=VS.getPlayer()
        if (not playa.isNull()):
                self.makeQuestPersistent()
                vec = playa.Position()
                vec = Vector.Add(vec,(30000,0,0))
                drone=VS.launch("IO47","drone","unknown","unit","default",1,1,vec,'')
                VS.AdjustRelation("unknown",playa.getFactionName(),-1,10);
                VS.AdjustRelation(playa.getFactionName(),"unknown",-1,10);
                drone.SetTarget(playa)
                self.stage=1
        else:
            drone=VS.Unit()
        
    def setDroneNear (self,playa):
        global drone
        vec = playa.Position()
        vec = Vector.Add (vec,(vsrandom.uniform(-1000,1000),
                               vsrandom.uniform(-1000,1000),
                               vsrandom.uniform(-1000,1000)))
        drone.SetCurPosition(vec)
        drone.SetTarget(playa)
    def Execute (self):
        global drone
        playa=VS.getPlayer()
        if (playa.isNull()):
            return 1
        if not quest.checkSaveValue(playa.isPlayerStarship(),'privateer_drone_active',1):
            return 1
        if playa!=self.savedplaya:
            self.setup()
        global derelict
        if VS.getSystemFile() == "Gemini/Delta_Prime":
            if derelict.isNull():
                generateBase()
        if (not self.stage):
            if (derelict and (VS.getSystemFile()==self.sysfile)):
                if (derelict.getSignificantDistance(playa)<1000):
                    print ("launch drone")
                    self.launchNewDrone()
            else:
                print ("launch drone")
                self.launchNewDrone()
        else:
            if (drone.isNull()):
                print ("no drone")
                self.removeQuest();
                return 0
            sf = VS.getSystemFile();
            if (self.sysfile!=sf and sf!='Gemini/Nitir' and not self.jumping):
                drone.JumpTo(sf);
                self.sysfile=sf
#                self.setDroneNear(playa)
                self.lastdist=10000
                self.jumping=1
                print ("jumping")
            else:
                if (self.jumping):
                    if (playa.getUnitSystemFile()==drone.getUnitSystemFile()):
                        drone.SetTarget (playa)
                        self.jumping=0
                        self.setDroneNear(playa)

        return 1

class quest_drone_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_drone")
    def create (self):
        return quest_drone()
