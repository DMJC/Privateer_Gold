import Base
import VS
import guilds
def Can():
	return guilds.CanMerchantGuild()

def MakeMerchantGuild(concourse,timeofdayignored="_day"):
	# create the initial merchant guild screen
	room0 = Base.Room ('Merchant_Guild')
	Base.Texture (room0, 'background', 'bases/merchant_guild/merchantguild.spr', 0, 0)
	Base.Texture (room0, 'mtg', 'bases/merchant_guild/mtg.spr', -0.0303125, -0.0097)

	template = "#MISSION_TYPE# MISSION:                                            (#MISSION_NUMBER# of #NUM_MISSIONS#)\n" \
		+    "#DESCRIPTION#"

	#initial_message = "\n\n\n\n" \
	#	+    "Thank you for visiting\n" \
	#	+    "the Merchants' Guild\n" \
	#	+    "\n\n" \
	#	+    "    Please select a\n" \
	#	+    "    mission disc\n"
	initial_message = "\n\n\n\n" \
		+    "                        Welcome to the\n" \
		+    "                       Merchants' Guild\n"

	many_missions = "\n\n\n\n" \
		+    "We are sorry, but your Merchants'\n" \
		+    "Guild records indicate that your mission\n" \
		+    "schedule is already full.\n" \
		+    "\n" \
		+    "Thank you for visiting the\n" \
		+    "Merchants' Guild\n"

	# talk to agent
	Base.Python (room0, 'talk_merchant', -0.0975, -0.133333, 0.1975, 0.416667, 'Talk_To_Guild_Master', 'bases/merchant_talk.py',0)

	# exits at bottom and right of screen
	Base.Link (room0, 'exit_merchant1', -1.0, -1.0, 2.0, 0.25, 'Exit', concourse)
	Base.Link (room0, 'exit_merchant2', 0.75, -0.75, 0.25, 1.75, 'Exit', concourse)

	# create the computer close-up screen
	room1 = Base.Room ('Merchant_Guild_Computer')
	Base.Texture (room1, 'background1', 'bases/merchant_guild/merchantguildcomp.spr', 0, 0)

	# links between rooms
	Base.Link(room0,'to_merch_comp',-0.3175, -0.103333, 0.195, 0.223333,'Computer',room1)
	Base.Link(room1,'from_merch_comp',-1.0, -1.0, 2.0, 0.25,'Exit',room0)

	# guild core
	guildroom=guilds.GuildRoom(guilds.guilds['Merchant'],room1,template,many_missions)
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/merchantcd1.spr",0.5759375,-0.7469), 0.2825, -0.793333, 0.205, 0.466667, guildroom, 3))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/merchantcd2.spr",0.5759375,-0.7469), 0.4075, -0.766667, 0.1325, 0.463333, guildroom, 2))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/merchantcd3.spr",0.5759375,-0.7469), 0.5375, -0.7, 0.1175, 0.42, guildroom, 1))
	guildroom.AddMissionButton(guilds.MissionButton(("bases/merchant_guild/merchantcd4.spr",0.5759375,-0.7469), 0.59, -0.676667, 0.13, 0.423333, guildroom, 0))
	#guildroom.AddAcceptButton(guilds.AcceptButton(("bases/merchant_guild/merchantguildcompon.spr",0.4061875,0.1358),-0.3625, -0.0966667, 0.8875, 0.876667,guildroom))
	guildroom.AddAcceptButton(guilds.AcceptButton(None,-0.3625, -0.0966667, 0.8875, 0.876667,guildroom))
	Base.TextBox(room1, 'merchantbox', initial_message, -0.3395, 0.7275, (0.5, -0.7954, 1), (0,0,0), 0, (140.0/255.0,210.0/255.0,140.0/255.0))
	Base.TextBox(room1, 'hack', '', -100, -100, (0, 0, 1), (0,0,0), 0, (1.0,1.0,1.0)) #Hack to fix missing glColor() in older VegaStrike versions
	Base.Texture(room1,  'compbkg', 'bases/merchant_guild/merchantguildcompon.spr',0.4061875,0.1358)
	guildroom.AddTextBox('merchantbox');
	guilds.CreateGuild(guildroom)
	return room0
