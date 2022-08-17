import Base
import dynamic_mission
import VS
import quest
import PlayerShip

# this uses the original coordinate system of Privateer
import GUI
GUI.GUIInit(320,200,0.03,0.03)

import land_hooks
land_hooks.run()

time_of_day=''
plist=VS.musicAddList('land.m3u')
VS.musicPlayList(plist)
dynamic_mission.CreateMissions()

# add Landing Pad
room0 = Base.Room ('Landing_Pad')
Base.Texture (room0, 'background', 'bases/perry/Perry_LandingBay'+time_of_day+'.spr', 0, 0)

PlayerShip.InitPlayerShips()
PlayerShip.AddPlayerShips('perry',room0,'landship')

Base.Texture (room0, 'lbl', 'bases/perry/Perry_LandingBay_lbl'+time_of_day+'.spr', 0.109125, -0.5529)

Base.LaunchPython (room0, 'my_launch_id', 'bases/launch_hooks.py', 0.24, -0.133333, 0.695, 0.52, 'Launch')

# add Main Concourse
room = Base.Room ('Perry_Concourse')
room1 = room
Base.Texture (room, 'stb', 'bases/perry/Perry_Concourse_sta'+time_of_day+'.spr', 0, 0)
Base.Texture (room, 'sh0', 'bases/perry/Perry_Concourse_sh0'+time_of_day+'.spr', 0, 0)
Base.Texture (room, 'background', 'bases/perry/Perry_Concourse'+time_of_day+'.spr', 0, 0)
Base.Texture (room, 'car', 'bases/perry/Perry_Concourse_car'+time_of_day+'.spr', 0, 0)

# add links between pad and concourse
Base.Link (room0, 'my_link_id', -1, -1, 2, 0.2, 'Main_Concourse', room1)
Base.Link (room0, 'my_link_id', -0.415, -0.13, 0.2875, 0.383333, 'Main_Concourse', room1)
Base.Link (room1, 'my_link_id', -0.98, -0.923333, 0.27, 0.856667, 'Landing_Pad', room0)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room0, room1)

# add Admiral Terrel's office
import campaign_lib
terrell_entry=(not quest.checkSaveValue(VS.getCurrentPlayer(),"terrell_no_entry",1.0)) and len(campaign_lib.getActiveCampaignNodes(room1))
if terrell_entry:
	room = Base.Room ('Admiral_Terrells_Office')
	room2 = room
	Base.Texture (room, 'background', 'bases/perry/Perry_AdmTerrelOffice'+time_of_day+'.spr', 0.582, -0.2716)
	Base.Texture (room, 'ltt', 'bases/perry/Perry_AdmTerrelOffice_ltt'+time_of_day+'.spr', -0.5053125, -0.1908)
	Base.Texture (room, 'trl', 'bases/perry/Perry_AdmTerrelOffice_trl'+time_of_day+'.spr', 0.5616875, -0.162)
	Base.Link (room1, 'my_link_id', 0.0625, -0.22, 0.0975, 0.12, 'Admiral_Terrell\'s_Office', room2)
	Base.Link (room2, 'my_link_id', -0.9675, -0.98, 0.3975, 0.48, 'Main_Concourse', room1)
	Base.Python (room2, 'my_link_id', 0.48, -0.24375, 0.1953125, 0.1953125, 'Talk_To_Admiral_Terrell', '#\nimport campaign_lib\nimport campaign_lib\ncampaign_lib.AddConversationStoppingSprite("Admiral_Terrell","bases/heads/terrell.spr",(.582,-.2716),(3.104,2.4832),"Return_To_Office").__call__('+str(room2)+',None)\ncampaign_lib.clickFixer('+str(room2)+')\n',False)
else:
	room = Base.Room ('Exit_Admirals_Office')
	room2 = room
	# No access to Admeral Ofise
	Base.Texture(room2, 'goodin','bases/heads/goodindoor.spr',.582,-.2716)
	Base.LinkPython (room1, 'my_link_id', '''#
import campaign_lib
campaign_lib.displayText('''+str(room2)+''',[("Goodin","Hey, where do you think you\'re going?","campaign/wheredoyouthinkyouregoing.ogg"),
	("Burrows","Just wandering around. Is there a problem?"),
	("Goodin","There is, if you try to go through that door. That\'s Admiral Terrell\'s office. He doesn\'t like visitors."),
	("Burrows","Hey, don\'t sweat it, sweetheart. I don\'t like visiting. Later.")])
''', 0.0625, -0.22, 0.0975, 0.12, 'Admiral_Terrell\'s_Office', room2)
	Base.LinkPython (room2, 'go_back','#\nimport VS\nVS.StopAllSounds()\n', -1, -1, 2, 2, 'Exit_Admirals_Office', room1)

# add commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room1, 0.305, -0.49, 0.245, 0.313333, 'Commodity_Exchange')

# add ship dealer
import weapons_lib
weapons_lib.basename="perry"
weap = weapons_lib.MakeWeapon (room1,time_of_day)
Base.Link (room1, 'weapon_room', 0.6375, -0.753333, 0.3275, 0.446667, 'Ship_Dealer/Upgrade', weap)

# add mission computer
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room1,time_of_day)
Base.Link (room1, 'my_comp_id', 0.8575, -0.0866667, 0.075, 0.106667, 'Mission_Computer', miscomp)

# add bar
import bar_lib
bar = bar_lib.MakeBar (room1,time_of_day,'military','bases/bar/Helen_Bar',quest.checkSaveValue(VS.getCurrentPlayer(),"terrell_no_entry",2.0) or not terrell_entry,True,'perry',False,[('pe0', -0.0909375, 0.0),('pe1', -0.8548125, -0.0388),('pe2', -0.55775, -0.2037),('pe3', -0.230375, -0.2037)])
Base.Link (room1, 'bar', 0.71, -0.0666667, 0.105, 0.2, 'Bar', bar)

# add guilds
import mercenary_guild
merchant = mercenary_guild.MakeMercenaryGuild (room1,time_of_day)
Base.Link (room1, 'mercenary', 0.6025, -0.0333333, 0.0825, 0.163333, 'Mercenary_Guild', merchant)
import merchant_guild
merchant = merchant_guild.MakeMerchantGuild (room1,time_of_day)
Base.Link (room1, 'merchant', 0.52, -0.01, 0.06, 0.146667, 'Merchant_Guild', merchant)

plist=VS.musicAddList('perry.m3u')
VS.musicPlayList(plist)
