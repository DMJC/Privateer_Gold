import Base
import VS
import guilds
def Can():
	return guilds.CanMercenaryGuild()

def MakeMercenaryGuild(concourse,timeofdayignored="_day"):
	# create the initial mercenary guild screen
	room0 = Base.Room ('Mercenary_Guild')
	Base.Texture (room0, 'background', 'bases/merchant_guild/mercernaryguild.spr', 0, 0)
	Base.Texture (room0, 'myg', 'bases/merchant_guild/myg.spr', 0.12125, 0.0388)
	Base.Texture (room0, 'psm', 'bases/merchant_guild/psm.spr', -0.7093125, 0.10185)
	
	template = "#MISSION_TYPE# MISSION:                                            (#MISSION_NUMBER# of #NUM_MISSIONS#)\n" \
		+    "#DESCRIPTION#"

	#initial_message = "\n\n\n\n" \
	#	+    "Thank you for visiting\n" \
	#	+    "the Mercenaries' Guild\n" \
	#	+    "\n\n" \
	#	+    "    Please select a\n" \
	#	+    "    mission disc\n"
	initial_message = "\n\n\n\n" \
		+    "                           Welcome to the\n" \
		+    "                         Mercenaries' Guild\n"

	many_missions = "\n\n\n\n" \
		+    "We are sorry, but your Mercenaries'\n" \
		+    "Guild records indicate that your mission\n" \
		+    "schedule is already full.\n" \
		+    "\n" \
		+    "Thank you for visiting the\n" \
		+    "Mercenaries' Guild\n"

	# talk to agent
	Base.Python (room0, 'talk_mercenary', -0.065, -0.17, 0.23, 0.506667, 'Talk_To_Receptionist', 'bases/mercenary_talk.py',0)

	# exits at bottom and right of screen
	Base.Link (room0, 'exit_mercenary1', -1.0, -1.0, 2.0, 0.25, 'Exit', concourse)
	Base.Link (room0, 'exit_mercenary2', 0.75, -0.75, 0.25, 1.75, 'Exit', concourse)

	# create the computer close-up screen
	room1 = Base.Room ('Mercenary_Guild_Computer')
	Base.Texture (room1, 'background1', 'bases/merchant_guild/mercernaryguildcomp.spr', 0, 0)
	Base.Texture (room1, 'psc', 'bases/merchant_guild/psc.spr', -0.776, -0.2716)

	# links between rooms
	Base.Link(room0,'to_merc_comp',-0.415, -0.226667, 0.335, 0.293333,'Computer',room1)
	Base.Link(room1,'from_merc_comp',-1.0, -1.0, 2.0, 0.25, 'Exit', room0)

	# guild core
	guildroom=guilds.GuildRoom(guilds.guilds['Mercenary'],room1,template,many_missions)
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/mercernarycd1.spr",0.6001875,-0.6887), 0.1825, -0.653333, 0.2575, 0.52, guildroom, 3))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/mercernarycd2.spr",0.6001875,-0.6887), 0.35, -0.713333, 0.2975, 0.593333, guildroom, 2))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/mercernarycd3.spr",0.6001875,-0.6887), 0.44, -0.683333, 0.345, 0.556667, guildroom, 1))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/mercernarycd4.spr",0.6001875,-0.6887), 0.66, -0.6, 0.3375, 0.496667, guildroom, 0))
	guildroom.AddAcceptButton(guilds.AcceptButton(None, -0.7325, -0.526667, 1.0175, 1.08667, guildroom))
	Base.TextBox(room1, 'mercenarybox', initial_message, -0.5925, 0.3967, (.24, -.55, 1), (0,0,0), 0, (148.0/255.0,140.0/255.0,60.0/255.0))
	Base.TextBox(room1, 'hack', '', -100, -100, (0, 0, 1), (0,0,0), 0, (1.0,1.0,1.0)) #Hack to fix missing glColor() in older VegaStrike versions
	guildroom.AddTextBox('mercenarybox');
	guilds.CreateGuild(guildroom)
	return room0
