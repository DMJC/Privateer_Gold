import Base
import dynamic_mission
import VS
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

# add landing pad
room_landing_pad = Base.Room ('Landing_Pad')
Base.Texture (room_landing_pad, 'background', 'bases/refinery/Edinburgh_LandingBay'+time_of_day+'.spr', 0, 0)
Base.Texture (room_landing_pad, 'str', 'bases/refinery/Edinburgh_LandingBay_lst'+time_of_day+'.spr', 0.2849375, 0.0388)
Base.Texture (room_landing_pad, 'lit', 'bases/refinery/lit'+time_of_day+'.spr', -0.183, 0.368)

PlayerShip.InitPlayerShips()
PlayerShip.AddPlayerShips('pleasure',room_landing_pad,'landship')

Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.33, -0.573333, 0.8475, 0.6, 'Launch')

# add main concourse
room_concourse = Base.Room ('Concourse')
Base.Texture (room_concourse, 'background', 'bases/refinery/Anapolis_Concourse'+time_of_day+'.spr', 0.582, -0.2716)
Base.Texture (room_concourse, 'str', 'bases/refinery/Anapolis_Concourse_str'+time_of_day+'.spr', 0.582, 0.6596)
Base.Texture (room_concourse, 'sh0', 'bases/refinery/Anapolis_Concourse_sh0'+time_of_day+'.spr', 0, 0.6529)
Base.Texture (room_concourse, 'sh1', 'bases/refinery/Anapolis_Concourse_sh1'+time_of_day+'.spr', 0, 0.6329)
Base.Texture (room_concourse, 'wk0', 'bases/agricultural/Helen_Concourse_wk0'+time_of_day+'.spr', 0, -0.6466)
Base.Texture (room_concourse, 'wk2', 'bases/agricultural/Helen_Concourse_wk2'+time_of_day+'.spr', 0.185, -0.2507)

# add links between pad and concourse
Base.Link (room_landing_pad, 'my_link_id', 0.6225, -0.416667, 0.2425, 0.5, 'Main_Concourse', room_concourse)
Base.Link (room_concourse, 'my_link_id', 0.035, -0.34, 0.28, 0.266667, 'Hangar', room_landing_pad)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)

# add bar
import bar_lib
bar = bar_lib.MakeBar (room_concourse,time_of_day, 'refinery', "bases/bar/Helen_Bar", True, True, 'refinery', False, [("rf0",-.230376,-.1934),("rf1",-.084875,-.0097),("rf3",-.8548125,-.0388),("rf2",-.55775,-.2037)])
Base.Link (room_concourse, 'bar', -0.5975, -0.133333, 0.17, 0.25, 'Bar', bar)

# add guilds
import merchant_guild
if (merchant_guild.Can()):
	merchant = merchant_guild.MakeMerchantGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'merchant', 0.03, 0.0933333, 0.22, 0.176667, "Merchant's Guild", merchant)
else:
	Base.Texture (room_concourse, 'nomerchant', 'bases/agricultural/nomerchant'+time_of_day+'.spr', 0.1455, 0.1552)

import mercenary_guild
if (mercenary_guild.Can()):
	merchant = mercenary_guild.MakeMercenaryGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'mercenary', 0.73, 0.0466667, 0.235, 0.14, 'Mercenary_Guild', merchant)
else:
	Base.Texture (room_concourse, 'nomercenary', 'bases/agricultural/nomercenary'+time_of_day+'.spr', 0.860875, 0.1067)

# add ship dealer
import weapons_lib
weapons_lib.basename="mining_base"
if (weapons_lib.CanRepair()):
	weap = weapons_lib.MakeWeapon (room_concourse,time_of_day)
	Base.Link (room_concourse, 'weapon_room', -0.545, -0.563333, 0.255, 0.36, 'Ship_Dealer/Upgrade', weap)
else:
	Base.Texture (room_concourse, 'noshipdealer', 'bases/agricultural/noshipdealer'+time_of_day+'.spr', -0.2606875, -0.4656)

# add commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room_concourse, 0.6475, -0.366667, 0.32, 0.206667, 'Commodity_Exchange')

# add mission computer
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room_concourse,time_of_day)
Base.Link (room_concourse, 'my_comp_id', 0.4075, -0.85, 0.15, 0.276667, 'Mission_Computer', miscomp)

plist=VS.musicAddList('refinery.m3u')
VS.musicPlayList(plist)