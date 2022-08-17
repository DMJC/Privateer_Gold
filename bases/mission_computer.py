import Base
import VS
import guilds

def MakeMissionComputer(concourse,timeofdayignored="_day",bkg=[('background1', 'bases/mission_computer/background.spr', 0.582, -0.2716),('yellowblink', 'bases/mission_computer/yellow_blink.spr', -0.582, 0.8924)],logon_bkg=None):
#	print "Making mission computer"
	print ("Making mission computer")

	template = "Available missions: #NUM_MISSIONS#\n" \
		+    "Current mission: #MISSION_NUMBER#\n" \
		+    "\n" \
		+    "#MISSION_TYPE# MISSION:\n" \
		+    "#DESCRIPTION#"

	initial_message = "\n" \
		+    ".\n" \
		+    ".\n" \
		+    ".\n" \
		+    ".\n" \
		+    "Logged on\n" \
		+    "\n\n" \
		+    "Proceed and check for\n" \
		+    "available random missions."

	logon_message = "\n\n\n\n" \
		+    "                           Welcome to a\n" \
		+    "                  First Sector Mission Machine,\n" \
		+    "\n\n" \
		+    "                             To activate,\n" \
		+    "                           place palm on\n" \
		+    "                        Image Recognition\n" \
		+    "                               Scanner."

	many_missions = "\n\n\n\n" \
		+    "We are sorry, but your records\n" \
		+    "indicate that your mission schedule\n" \
		+    "is already full.\n" \
		+    "\n" \
		+    "Thank you for visiting a First Sector\n" \
		+    "Mission Machine\n"


	#logged-on computer room
	room = Base.Room ('Mission_Computer')
	if bkg and type(bkg)==list and len(bkg)>1:
		for spr in bkg:
			if spr and type(spr)==tuple and len(spr)>3:
				Base.Texture (room, spr[0], spr[1], spr[2], spr[3])
	else:
		#WARN!
#		print "No background specified for mission computer!\n"
		print ("No background specified for mission computer!\n")
	Base.Link(room,'to_concourse',-1, -1, 2, 0.15,'Return_To_Concourse',concourse)

	if not logon_bkg:
		logon_bkg = bkg

	#logon screen
	logon = Base.Room ('Mission_Computer_(logged_off)')
	if logon_bkg and type(logon_bkg)==list and len(logon_bkg)>1:
		for spr in logon_bkg:
			if spr and type(spr)==tuple and len(spr)>3:
				Base.Texture (logon, spr[0], spr[1], spr[2], spr[3])
	else:
		#WARN!
#		print "No background specified for mission computer logon screen!\n"
		print ("No background specified for mission computer logon screen!\n")
	Base.TextBox (logon, 'logontext'  , logon_message, -0.618375, 0.6499, (0.303125, -0.44135, 1), (0,0,0), 0, (221.0/255.0,4.0/255.0,0.0))
	Base.Link(logon,'log_on',0.1875,-0.8,0.4375,0.3,'Activate_Computer',room)
	Base.Link(logon,'to_concourse',-1, -1, 2, 0.15,'Return_To_Concourse',concourse)

	guildroom=guilds.GuildRoom(guilds.guilds['Computer'],room,template,many_missions)

	#invisible mission buttons - needed by guildroom
	for i in range(guildroom.guild.maxmissions):
		guildroom.AddMissionButton(guilds.MissionButton(("",0,0), 10, 10, 0, 0, guildroom, i, 0)) #invisible

	#other mission buttons
	guildroom.AddMissionButton(guilds.MissionButton(("bases/mission_computer/last.spr"  ,-0.56078125,-0.6305), -0.6486875, -0.776 , 0.194  , 0.3104 , guildroom, 'last'))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/mission_computer/next.spr"  ,-0.31828125,-0.6305), -0.41225  , -0.776 , 0.194  , 0.3104 , guildroom, 'next'))
	guildroom.AddAcceptButton (guilds.AcceptButton (("bases/mission_computer/accept.spr",-0.05153125,-0.6305), -0.181875 , -0.7275, 0.2425 , 0.2425 , guildroom))

	#load/save link
#	Base.Comp (logon,'my_comp_id', 0.351625, -0.2328, 0.2243125, 0.7566, 'Load/Save', 'Info ')
#	Base.Comp (room, 'my_comp_id', 0.351625, -0.2328, 0.2243125, 0.7566, 'Load/Save', 'Info ')

	Base.TextBox(room, 'miscompbox', initial_message, -0.618375, 0.6499, (0.303125, -0.44135, 1), (0,0,0), 0, (221.0/255.0,4.0/255.0,0.0))
	Base.TextBox(room, 'hack', '', -100, -100, (0, 0, 1), (0,0,0), 0, (1.0,1.0,1.0)) #Hack to fix missing glColor() in older VegaStrike versions
	guildroom.AddTextBox('miscompbox');
	guilds.CreateGuild(guildroom)

#	print "Made mission computer"
	print ("Made mission computer")
	return logon
