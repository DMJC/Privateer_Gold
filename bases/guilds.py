import mission_lib
import vsrandom
import Base
import VS
import quest
# import Director
import fixers

import custom

def CanX(disallowed):
	import universe
	sys = VS.getSystemFile()
	(name,fullname)=universe.getDockedBaseName()
	if sys in disallowed or name in disallowed or fullname in disallowed or (sys,name) in disallowed or (sys,fullname) in disallowed:
		return False
	return True
# lists from http://home.iprimus.com.au/Wedge009/Priv/Bases.html
# and http://www.djgallagher.com/games/pc/privateer/planets.php
def CanMerchantGuild():
	no_merchant={
		"Gemini/Capella":1,
		"Gemini/Delta_Prime":1,
		"Gemini/Eden":1,
		'Gemini/Hyades':1,
		'Gemini/KM-252':1,
		'Gemini/Lisacc':1,
		'Basra':1, # Gemini/Palan
		'Gemini/Pentonville':1,
		'Anapolis':1, # Gemini/Perry
		'Gemini/Ragnarok':1,
		'Vishnu':1, # Gemini/Rikel
		'Gemini/Rygannon':1,
		'Gemini/Sherwood':1,
		'Gemini/Telar':1,
		'Rilke':1, # Gemini/Varnus
		}
	return CanX(no_merchant)
def CanMercenaryGuild():
	no_mercenary={
		"Gemini/Capella":1,
		"Gemini/Delta_Prime":1,
		"Gemini/Eden":1,
		"Meadow":1, # Gemini/Hind's variable n
		"Gemini/Hyades":1,
		"Burton":1, # Gemini/Junction
		"Gemini/KM-252":1,
		"Thisbury":1, # Gemini/Manchester
		"Edinburgh":1, # Gemini/New Caledonia
		"Edom":1,# Gemini/New_Constantinople
		"Gemini/Nitir":1,
		"Gemini/Padre":1,
		"Palan":1, # Gemini/Palan
		"Gemini/Pentonville":1,
		"Gemini/Prasepe":1,
		"New_Iberia":1, # Gemini/Pyrenees
		"Gemini/Ragnarok":1,
		"Gracchus":1, # Gemini/Raxis
		"Siva":1, # Gemini/Rikel
		"Gemini/Shangri_La":1,
		"Gemini/Sherwood":1,
		"Gemini/Surtur":1,
		"Gemini/Telar":1,
		"Bodensee":1, # Gemini/Tingerhoff
		"Helen":1, # Gemini/Troy
		"Rilke":1, # Gemini/Varnus
		"Joplin":1, # Gemini/XXN-1927
		}
	return CanX(no_mercenary)

class GenericGuild:
	def __init__(self, name, min, max, missiontypes, membership, prefix='#G#', acceptmsg='', tech=[]):
		"""Initializes the guild"""
		self.name=name.split('/')[0]
		self.missions=missiontypes
		self.minmissions=min
		self.maxmissions=max
		self.nummissions=-1
		self.savestring="Joined"+self.name+"Guild"
		self.membership=membership
		self.tech=tech
		self.prefix=prefix
		self.acceptMessage=acceptmsg
		self.tooManyMissionsTrigger = 4
	
	def CanTakeMoreMissions(self):
		return (VS.numActiveMissions()<self.tooManyMissionsTrigger)
		
	def MakeMissions(self):
		"""Creates the missions using the mission_lib interface"""
		self.nummissions=vsrandom.randrange(self.minmissions,self.maxmissions+1)
		self.nummissions=mission_lib.CreateGuildMissions(self.name, self.nummissions, self.missions, self.prefix, self.acceptMessage)
		return ["success", self.nummissions]
	
	def HasJoined(self):
		if (self.membership<=0):
			return True;
		else:
			plr=VS.getPlayer().isPlayerStarship()
			return quest.checkSaveValue(plr,self.savestring)
	
	def CanPay(self):
            return (self.membership<=0) or (self.membership<VS.getPlayer().getCredits())
	
	def Join(self):
		plr=VS.getPlayer()
		plrnum=plr.isPlayerStarship()
		if self.CanPay():
			quest.removeQuest(plrnum,self.savestring,1)
			plr.addCredits(-1*self.membership)
			for tt in self.tech:
				import universe
				universe.addTechLevel(tt)
			self.MakeMissions()
			return ["success"]
		else:
			return ["failure"]
	
	def Accept(self, missionname):
		if not self.CanTakeMoreMissions():
			return ["toomany"]
		else:
			mission_lib.SetLastMission(missionname);
			if mission_lib.LoadLastMission():
				return ["success"]
			else:
				return ["notavailable","Mission no longer available"]
		
	def handle_server_cmd(self,cmd,args):
		if cmd=='join':
			return self.Join()
		if not self.HasJoined():
			return ["failure", "You have not joined this guild yet!"]
		if cmd=='accept':
			return self.Accept(args[0])
		elif cmd=='MakeMissions':
			return self.MakeMissions()

class Guild(GenericGuild):
	"""Stores information about the guild itself (name, mission types, number of missions)"""
	def __init__(self, name, min, max, missiontypes, membership, prefix='#G#', acceptmsg='', tech=[]):
		GenericGuild.__init__(self, name, min, max, missiontypes, membership, prefix, acceptmsg, tech)
	
	def RequestJoin(self):
		def JoinStatus(args):
			if args[0]=="success":
				Base.Message('Thank you for joining the '+str(self.name)+' Guild! Feel free to accept any of our large quantity of high-paying missions.')
				VS.playSound("guilds/"+str(self.name).lower()+"accept.wav",(0,0,0),(0,0,0))
			else:
				Base.Message('We have checked your account and it appears that you do not have enough credits to join this guild. Please come back and reconsider our offer when you have received more credits.')
				VS.playSound("guilds/"+str(self.name).lower()+"notenoughmoney.wav",(0,0,0),(0,0,0))
		plr=VS.getPlayer()
		plrnum=plr.isPlayerStarship()
		VS.StopAllSounds()
		if self.CanPay():
			custom.run('guilds',[self.name,'join'], JoinStatus)
		else:
			joinStatus(["failure"])


def handle_guilds_message(local, cmd, args, id):
	un = VS.getPlayer()
	plr = un.isPlayerStarship()
	if VS.isserver():
		import server
		if not server.getDocked(un):
			return ["failure", 'Not currently docked']
	guildinfo = guilds.get(args[0],None)
	if not guildinfo:
		return ["failure", 'Guild '+str(args[0])+' does not exit'];
	else:
		return guildinfo.handle_server_cmd(args[1], args[2:])

custom.add("guilds", handle_guilds_message)

class Button:
	"""A button that you can click on."""
	def __init__(self,spritefile,x,y,wid,hei,room,linkdesc,index,pythonstr):
		"""Initializes the button (but does not draw it; use drawobjs())"""
		self.sprite=spritefile
		self.x=x
		self.y=y
		self.wid=wid
		self.hei=hei
		self.room=room
		self.linkdesc=linkdesc
		self.index=index
		self.pythonstr=pythonstr
		self.state=0
	
	def drawobjs(self):
		"""Creates the button in the guild room"""
		if self.state==0:
			Base.Python(self.room,self.index,self.x,self.y,self.wid,self.hei,self.linkdesc,self.pythonstr,True)
			if self.sprite and type(self.sprite)==tuple and len(self.sprite)>2:
				Base.Texture(self.room,self.index,self.sprite[0],self.sprite[1],self.sprite[2])
			self.state=1
	
	def removeobjs(self):
		"""Hides the button"""
		if self.state==1:
			Base.EraseLink(self.room,self.index)
			if self.sprite and type(self.sprite)==tuple and len(self.sprite)>2:
				Base.EraseObj(self.room,self.index)
			self.state=0

class AcceptButton(Button):
	def __init__(self,spritefile,x,y,wid,hei,guildroom):
		Button.__init__(self,spritefile,x,y,wid,hei,guildroom.room,"Accept this Mission","accept","#G#\nimport guilds\nguilds.AcceptMission("+str(guildroom.room)+",'"+guildroom.guild.name+"')")
		self.guild=guildroom

class MissionButton(Button):
	def __init__(self,spritefile,x,y,wid,hei,guildroom,missionnum,visible=1):
		if visible:
			if isinstance(missionnum,type(int())):
				pythonstr='#G#\nimport guilds\nguilds.SetCurrentMission('+str(guildroom.room)+",'"+guildroom.guild.name+"',"+str(missionnum)+')'
				desc="View Mission Description (Mission " + str(missionnum+1)+")"
			else:
				pythonstr='#G#\nimport guilds\nguilds.SetCurrentMission('+str(guildroom.room)+",'"+guildroom.guild.name+"','"+str(missionnum)+"')"
				desc="View "+str(missionnum)+" Mission Description"
			Button.__init__(self,spritefile,x,y,wid,hei,guildroom.room,desc,"missiondesc_guild_"+guildroom.guild.name+"_"+str(missionnum),pythonstr)
		self.guild=guildroom
		self.missionnum=missionnum
		self.missionname=guildroom.guild.name+'/'+str(missionnum)
		self.isactive=False
		self.visible=visible
	
	def select(self):
		if not self.guild.CanTakeMoreMissions():
			self.guild.TooManyMissions()
		else:
			self.removeobjs()
			mission_lib.BriefLastMission(self.missionname,0,self.guild.textbox,self.guild.briefingTemplate)
	
	def deselect(self):
		self.drawobjs()

	def removeobjs(self):
		if self.visible:
			Button.removeobjs(self)

	def drawobjs(self):
		if not self.isactive:
			if self.visible and (not isinstance(self.missionnum,type(int())) or self.missionnum<self.guild.guild.nummissions):
				Button.drawobjs(self)
	
	def accept(self):
#		print "MISSION XNAME "+self.missionname
		print ("MISSION XNAME "+self.missionname)
		if not self.guild.CanTakeMoreMissions():
			self.guild.TooManyMissions()
		else:
			self.isactive=True
			self.removeobjs()
			mission_lib.SetLastMission(self.missionname);
			def completeAccept(args):
				if VS.networked():
					if args[0]=="success" or args[0]=="notavailable":
						mission_lib.BriefLastMission(self.missionname,1,self.guild.textbox)
						mission_lib.RemoveLastMission(self.missionname)
				if args[0]=="toomany":
					self.guild.TooManyMissions()
				if args[0]=="notavailable":
					self.guild.CargoFull()
			if not VS.networked():
				mission_lib.BriefLastMission(self.missionname,1,self.guild.textbox)
			custom.run("guilds",[self.guild.guild.name,"accept",self.missionname],completeAccept)
			
#			Base.Message('Thank you. We look forward to the completion of your mission.')

class GuildRoom:
	"""Stores information about this instance of the guild room in this base."""
	def __init__(self,guild,room,briefingTemplate='#DESCRIPTION#',tooManyMissionsText='You are already doing too many missions.\nFinish those first, and then come back.'):
		self.buttons={}
		self.acceptbutton=None
		self.textbox=None
		self.guild=guild
		self.room=room
		self.missionnum=-1
		self.briefingTemplate=briefingTemplate
		self.tooManyMissionsText = tooManyMissionsText
		self.tooManyMissionsTrigger = 4 #1 more than the actual value
	
	def AddMissionButton(self,button):
		self.buttons[button.missionnum]=button
	
	def AddAcceptButton(self,abutton):
		self.acceptbutton=abutton
	
	def AddTextBox(self,textbox):
		self.textbox=textbox
	
	def AcceptMission(self):
		if self.missionnum>=0:
			self.buttons[self.missionnum].accept()
			self.missionnum=-1

	def TooManyMissions(self):
		Base.SetTextBoxText(Base.GetCurRoom(),self.textbox,self.tooManyMissionsText)
		self.acceptbutton.removeobjs()
		if 'next' in self.buttons:
			self.buttons['next'].removeobjs()
		if 'last' in self.buttons:
			self.buttons['last'].removeobjs()
	def CargoFull(self):
		Base.SetTextBoxText(Base.GetCurRoom(),self.textbox,"Insufficient Cargo Space")

	def CanTakeMoreMissions(self):
		return self.guild.CanTakeMoreMissions()
	
	def SetCurrentMission(self,missionnum):
		if missionnum == 'next':
			missionnum = self.missionnum + 1
			while missionnum < self.guild.nummissions and self.buttons[missionnum].isactive:
				missionnum = missionnum + 1
			if missionnum >= self.guild.nummissions:
				missionnum = self.guild.nummissions - 1
			while missionnum >= 0 and self.buttons[missionnum].isactive:
				missionnum = missionnum - 1
		if missionnum == 'last':
			missionnum = self.missionnum - 1
			while missionnum >= 0 and self.buttons[missionnum].isactive:
				missionnum = missionnum - 1
			if missionnum < 0:
				missionnum = 0
			while missionnum < self.guild.nummissions and self.buttons[missionnum].isactive:
				missionnum = missionnum + 1

		if self.missionnum>=0:
			self.buttons[self.missionnum].deselect()
		for a in self.buttons:
			self.buttons[a].removeobjs()
		for a in self.buttons:
			self.buttons[a].drawobjs()
		self.missionnum=int(missionnum)
#		print str(self.missionnum)
		print (str(self.missionnum))
		if self.missionnum>=0:
			self.buttons[self.missionnum].select()

		if self.CanTakeMoreMissions():
			if self.missionnum>=0:
				self.acceptbutton.drawobjs()
			else:
				self.acceptbutton.removeobjs()

			if 'next' in self.buttons:
				mis = self.missionnum+1
				while (mis < self.guild.nummissions) and (self.buttons[mis].isactive):
					mis = mis + 1
				if (mis < self.guild.nummissions) and (not self.buttons[mis].isactive):
					self.buttons['next'].drawobjs()
				else:
					self.buttons['next'].removeobjs()
			if 'last' in self.buttons:
				mis = self.missionnum-1
				while (mis >= 0) and (self.buttons[mis].isactive):
					mis = mis - 1
				if (mis >= 0) and (not self.buttons[mis].isactive):
					self.buttons['last'].drawobjs()
				else:
					self.buttons['last'].removeobjs()
	
	def drawobjs(self):
#		print 'len buttons'
#		print len(self.buttons)
#		print 'num missions'
#		print self.guild.nummissions
#		print 'button list'
#		print self.buttons
		print ('len buttons')
		print (len(self.buttons))
		print ('num missions')
		print (self.guild.nummissions)
		print ('button list')
		print (self.buttons)
		for m in self.buttons:
#			print 'draw button'
			print ('draw button')
			if not isinstance(m,type(int())) or m < self.guild.nummissions:
				self.buttons[m].drawobjs()

guildrooms={}
guilds={
	'Merchant'  :  Guild('Merchant',  3, 4, { 'Escort':1, 'Cargo' :3 }, 1000.00, '#G#', '\n\n\n\nMission accepted.\n\nThank you.', []),  #["merchant"]), #no more tech, [] instead
	'Mercenary' :  Guild('Mercenary', 3, 4, { 'Bounty':3, 'Defend':1 }, 5000.00, '#G#', '\n\n\n\nMission accepted.\n\nThank you.', []),  #["hunter"]) # no more tech, [] instead
	'Computer'  :  Guild('Computer',  4, 6, { 'Rescue':2, 'Patrol':2, 'Defend':2, 'Bounty':2, 'Wingman':0, '*':1 }, 0, '#C#', '\n\n\n\nMission accepted.\n\nThank you.', [])              # Base computer interface (it's a guild - go figure)
	}
def AcceptMission(room,guildname):
	if guildname in guildrooms:
		for guildroom in guildrooms[guildname]:
			if guildroom.room==room:
				guildroom.AcceptMission()
				return True
	return False

def SetCurrentMission(room,guildname,missionnum):
	if guildname in guildrooms:
		for guildroom in guildrooms[guildname]:
			if guildroom.room==room:
				guildroom.SetCurrentMission(missionnum)
				return True
	return False
def JoinGuild(guildname):
	guilds[guildname].RequestJoin()
	fixers.DestroyActiveButtons()
#	print 'Create it ' + guildname
	print ('Create it ' + guildname)
	if guildname in guildrooms:
#		print 'Create it ' + str(guildrooms[guildname])
		print ('Create it ' + str(guildrooms[guildname]))
		for guildroom in guildrooms[guildname]:
#			print "drawing"
			print ("drawing")
			CreateJoinedGuild(guildname, guildroom)

def TalkToReceptionist(guildname,introtext):
	text=introtext
	import campaign_lib
	if campaign_lib.doTalkingHeads():
		campaign_lib.AddConversationStoppingSprite("Receptionist","bases/heads/"+guildname.lower()+".spr",(.582,-.2716),(3.104,2.4832),"Return_To_Guild").__call__(Base.GetCurRoom(),None)
#	print 'start ('+str(guildname)+','+str(introtext)+')'
	print ('start ('+str(guildname)+','+str(introtext)+')')
	if guildname in guilds:
		guild=guilds[guildname]
		if not guild.HasJoined():
			text+='  Membership is '+str(guild.membership)+' credits.  Please consider joining our guild'
			if not guild.CanPay():
				text+=' when you have more money'
			text+='.'
		Base.Message (text)
		if not guild.HasJoined():
			VS.StopAllSounds()
			if guild.CanPay():
				fixers.CreateChoiceButtons(Base.GetCurRoom(),[
					fixers.Choice("bases/fixers/yes.spr","#G#\nimport guilds\nguilds.JoinGuild('"+guildname+"')","Accept This Agreement"),
					fixers.Choice("bases/fixers/no.spr","bases/fixers/"+str(guild.name).lower()+"no.py","Decline This Agreement")])

				VS.playSound("guilds/"+str(guild.name).lower()+"invite.wav",(0,0,0),(0,0,0))
			else:
				VS.playSound("guilds/"+str(guild.name).lower()+"notenoughmoney.wav",(0,0,0),(0,0,0))			
		return

def CreateJoinedGuild(guildname,guildroom):
#	print 'has joined.'
	print ('has joined.')
	if not VS.networked():
#		print 'make missions'
		print ('make missions')
		guildroom.guild.MakeMissions()
		guildroom.drawobjs()
	else:
		def MakeStatus(args):
			if args[0]=='success':
				guildroom.guild.nummissions = int(args[1])
				guildroom.drawobjs()
			else:
#				print "MakeMissions call returned "+str(args)
				print ("MakeMissions call returned "+str(args))
		custom.run('guilds',[guildname,'MakeMissions'], MakeStatus)

def CreateGuild(guildroom):
	guildname=guildroom.guild.name
#	print 'Create it ' + guildname
	print ('Create it ' + guildname)
#	if guildname in guildrooms:
#		guildrooms[guildname].append(guildroom)
#	else:
	if True:
		guildrooms[guildname]=[guildroom]
#		print 'true'
		print ('true')
		if guildroom.guild.HasJoined():
			CreateJoinedGuild(guildname,guildroom)

def Clear():
	del guildrooms
	guildrooms={}

