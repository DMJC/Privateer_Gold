import Base
import dynamic_mission
import VS
import quest
import campaign_lib
import PlayerShip

def MakeUniversity (time_of_day='_day'):

	# this uses the original coordinate system of Privateer
	import GUI
	GUI.GUIInit(320,200,0.03,0.03)

	campaign_lib.masterson_extraspeech=""

	plist=VS.musicAddList('land.m3u')
	VS.musicPlayList(plist)
	dynamic_mission.CreateMissions()

	plist=VS.musicAddList('oxford.m3u')
	VS.musicPlayList(plist)	

	# add main landing pad
	room0 = Base.Room ('Landing_Pad')
	Base.Texture (room0, 'background', 'bases/university/Landing_Pad.spr', 0, 0)
	Base.Texture (room0, 'tnl00000', 'bases/university/Landing_Pad_tnl00000.spr', 0, 0)

	PlayerShip.InitPlayerShips()
	PlayerShip.AddPlayerShips('university',room0,'landship')

	Base.LaunchPython (room0, 'my_launch_id', 'bases/launch_hooks.py', -0.0075, -0.59, 0.4725, 0.31, 'Launch')

	# add landing pad with moving train
	room0train = Base.Room ('Landing_Pad')
	Base.Texture (room0train, 'background', 'bases/university/Landing_Pad.spr', 0, 0)

	PlayerShip.AddPlayerShips('university',room0train,'landship')
	
	# add main concourse
	room1 = Base.Room ('Campus_Quad')
	Base.Texture (room1, 'background', 'bases/university/Main_Quad.spr', 0.582, -0.2716)
	Base.Texture (room1, 'tnc', 'bases/university/Main_Quad_tnc.spr', -0.776, -0.9603)
	Base.Texture (room1, 'wk0', 'bases/university/Main_Quad_wk0.spr', -0.010125, 0.1)
	Base.Texture (room1, 'brd', 'bases/university/Main_Quad_brd.spr', 0.1273125, -0.4074)

	# Create the Quine 4000 screens
	import computer_lib
	room_personal_computer = computer_lib.MakePersonalComputer(room0, room1)

	# add library
	room2 = Base.Room ('Library_Stacks')
	denied=False
	if quest.checkSaveValue(VS.getPlayer().isPlayerStarship(),"access_to_library",2):
		denied=True
	the_campaigns=campaign_lib.getActiveCampaignNodes(room2)
	if quest.checkSaveValue(VS.getPlayer().isPlayerStarship(),"access_to_library",2):
		denied=True
	if quest.checkSaveValue(VS.getPlayer().isPlayerStarship(),"access_to_library",1): # access granted
		# Library stacks
		Base.Texture (room2, 'background', 'bases/university/Library_Main.spr', 0, 0)

		# Computer
		room3 = Base.Room ('Library_Terminal')
		Base.Texture (room3, 'background', 'bases/university/ComputerMain.spr', 0, 0)
		
		# Computer analyzing artifact
		room4 = Base.Room ('Library_Terminal')
		Base.Texture (room4, 'background', 'bases/university/ComputerMain.spr', 0, 0)
		Base.Texture (room4, 'background', 'bases/university/ComputerAnalysing.spr', 0, 0)

		# computer with Monkhouse text
		room5 = Base.Room ('Library_Terminal')
		Base.Texture (room5, 'background', 'bases/university/Monkhouse.spr', 0, 0)

		# links
		Base.Link (room2, 'my_link_id', 0.5, -0.5, 0.5, 1.5, 'Oxford_Square', room1)
		Base.Link (room2, 'my_link_id', -0.5, -1.0, 1.5, 0.4, 'Research_Computers', room3)
		Base.Link (room3, 'my_link_id', 0.105, -0.756667, 0.77, 0.8, 'Analyze_Artifact', room4)
		Base.Link (room3, 'my_link_id', -1.0, -1.0, 2.0, 1.95, 'Exit', room2)
		Base.Link (room4, 'my_link_id', 0.1025, -0.75, 0.77, 0.783333, 'Read_Computer_Screen', room5)
		Base.Link (room4, 'my_link_id', -1.0, -1.0, 2.0, 0.25, 'Exit', room2)
		Base.Link (room5, 'my_link_id', -1, -1, 2, 2, 'Turn_Off_Computer', room3)
		if denied:
			Base.Texture(room2,'masterson_access', 'bases/university/masterson.spr', 0, 0)
			##campaign_lib.clickFixer(room2)
			Base.Python(room2,'masterson_access', -1, -1, 2, 2, 'Enter_Library',
				"#\nimport Base\nBase.EraseLink("+str(room2)+", 'masterson_access')\nBase.EraseObj("+str(room2)+", 'masterson_access')\n", False)
			campaign_lib.masterson_extraspeech="barspeech/campaign/mastersonfinal.wav"
	else:
		Base.Texture (room2, 'background', 'bases/university/masterson.spr', 0, 0)
		##campaign_lib.clickFixer(room2)
		if len(the_campaigns) and denied: # mission in progress.
			Base.LinkPython(room2, 'masterson_return', '#\nimport campaign_lib\n##campaign_lib.clickFixer('+str(room2)+')\n', -1, -1, 2, 2, 'Exit_Library', room1)
		else: # Access denied. Come back after Lynch missions
			campaign_lib.displayText(room2, [("Masterson","Excuse me, where do you think you're going?"),
				("Burrows","I have some personal research I need to conduct."),
				("Masterson","I'm sorry, sir, but access to the Oxford library files is restricted to students."),
				("Burrows","Look, couldn't I just buy a library card?"),
				("Masterson","I'm afraid not. Good day to you, sir.")])
			campaign_lib.masterson_extraspeech="campaign/onlyforstudents-priv.ogg"
			Base.LinkPython(room2, 'masterson_return','#\nimport VS\nVS.StopAllSounds()\n', -1, -1, 2, 2, 'Exit_Library', room1)

	# add animated link from landing pad to university
	Base.LinkPython (room0, 'my_link_id', '''#
import Base
Base.Texture ('''+str(room0train)+''', "tnl", "bases/university/Landing_Pad_tnl.spr", 0, 0)
Base.RunScript('''+str(room0train)+''', "trainleave", """#
import Base
Base.SetCurRoom('''+str(room1)+''')
Base.EraseObj('''+str(room0train)+''',"tnl")
Base.EraseObj('''+str(room0train)+''',"trainleave")
""", 3.2)
''', 0.4225, -0.103333, 0.5425, 0.466667, 'Train_To_Oxford_University', room0train)
	# add link 
	Base.Link (room1, 'my_link_id', -0.9675, -0.97, 0.595, 0.923333, 'Train_To_Landing_Pad', room0)

	# add mission computer
	import mission_computer
	miscomp = mission_computer.MakeMissionComputer (room1,time_of_day)
	Base.Link (room1, 'my_comp_id', -0.5925, 0.293333, 0.09, 0.213333, 'Mission_Computer', miscomp)
#	print "Linked mission computer"
	print ("Linked mission computer")

	# add ship dealer
	import weapons_lib
	weapons_lib.basename="university"
	weap = weapons_lib.MakeWeapon (room1,time_of_day,"bases/university/Oxford_Shipdealer")
	Base.Link (room1, 'weapon_room', 0.695, -0.88, 0.2875, 0.913333, 'Ship_Dealer', weap)
	Base.SetLinkArea(weap, 'exit1_to_concourse',  -0.47, 0.50, 0.1725, 0.293333)
	Base.SetLinkArea(weap, 'exit2_to_concourse',  0.315, 0.0533333, 0.3175, 0.24)
	Base.SetLinkArea(weap, 'repair_bay_link', -0.2675, 0.336667, 0.66, 0.45)
	Base.SetLinkText(weap, 'exit1_to_concourse', "Oxford_Square")
	Base.SetLinkText(weap, 'exit2_to_concourse', "Oxford_Square")

	# add commodity exchange
	import commodity_lib
	commodity_lib.MakeCommodityLink (room1, 0.09, -0.973333, 0.5275, 0.34, 'Commodity_Exchange')

	# add bar
	import bar_lib
	bar = bar_lib.MakeBar (room1,time_of_day,"oxford","bases/university/Bar",False,False,None,False,[],"oxford")
	Base.Link (room1, 'bar', -0.9725, 0.0966667, 0.2325, 0.666667, 'Campus_Bar', bar)

	# add guilds
	import mercenary_guild
	merchant = mercenary_guild.MakeMercenaryGuild (room1,time_of_day)
	Base.Link (room1, 'mercenary', -0.53, 0.516667, 0.2, 0.456667, 'Mercenary_Guild', merchant)
	import merchant_guild
	merchant = merchant_guild.MakeMerchantGuild (room1,time_of_day)
	Base.Link (room1, 'merchant', -0.2625, 0.593333, 0.1375, 0.39, 'Merchant_Guild', merchant)

	# add link to library
	Base.LinkPython (room1, 'my_link_id','#\nimport campaign_lib\ncampaign_lib.clickFixer('+str(room2)+')\nif campaign_lib.masterson_extraspeech!="":\n\timport VS\n\tVS.playSound(campaign_lib.masterson_extraspeech,(0.,0.,0.),(0.,0.,0.,))\n\tcampaign_lib.masterson_extraspeech=""\n', 0.34, 0.45, 0.6375, 0.513333, 'Library', room2)
	#Base.Link (room1, 'my_link_id', 0.36, 0.696667, 0.0625, 0.0966667, 'Talk_To_Masterson', room5)

	return room1
