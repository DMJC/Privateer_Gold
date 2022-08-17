import cleansweep
import VS
class tripatrol(cleansweep.cleansweep):
	def __init__(self,numsystemsaway, num_points,distance,creds,jumps,donevar,minships,maxships,encounterprob,capshipprob,faction, forceattack,canrunaway,pirategreeting):	
		cleansweep.cleansweep.__init__(self,numsystemsaway, num_points,distance,creds,jumps,donevar,minships,maxships,encounterprob,capshipprob,faction, forceattack,canrunaway)
		self.pirategreeting=pirategreeting
		self.tricounter=16
		self.launchedpirate=False
		self.cp=VS.getCurrentPlayer()
	def RealSuccessMission(self):
		cleansweep.cleansweep.RealSuccessMission(self)
		print ("REAL SUCCESS")
		if (not self.launchedpirate):
			print ("LAUNCHING PIRATE")
			self.launchedpirate=True
			import launch
			L= launch.Launch()
			L.faction="pirates"
			L.fg="Drake"
			L.dynfg="" 
			L.minradius=500.0
			L.maxradius=550.0
			L.ai="default"
			L.num=1
			import faction_ships
			L.type=faction_ships.getRandomFighter("pirates")
			pirate=L.launch(self.you)
			import universe
			universe.greet(self.pirategreeting,pirate,self.you)
			print (pirate.getName())
			pirate.SetTarget(universe.getRandomJumppoint())
			pirate.ActivateJumpDrive(0)
			pirate.SetVelocity((0,0,1000))
	def Execute(self):
		if (VS.getPlayer()==self.you):
			self.tricounter-=1
			if (self.tricounter==8):
				VS.LoadMission("patroldeath.mission")
			if (self.tricounter==0):
				VS.LoadMission("patrolwar.mission");
		cleansweep.cleansweep.Execute(self)
