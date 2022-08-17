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
Base.Texture (room_landing_pad, 'background', 'bases/pleasure/Jolson_LandingBay'+time_of_day+'.spr', 0, 0)
Base.Texture (room_landing_pad, 'background', 'bases/pleasure/Jolson_LandingBay_wtr'+time_of_day+'.spr', 0, 0)
Base.Texture (room_landing_pad, 'background', 'bases/pleasure/Jolson_LandingBay_blt'+time_of_day+'.spr', 0.3576875, -0.0582)

PlayerShip.InitPlayerShips()
PlayerShip.AddPlayerShips('agricultural',room_landing_pad,'landship')

Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.3125, -0.543333, 0.8975, 0.54, 'Launch')

# add main concourse
room_concourse = Base.Room ('Main_Concourse')
Base.Texture (room_concourse, 'background', 'bases/agricultural/Helen_Concourse'+time_of_day+'.spr', 0.582, -0.2716)
Base.Texture (room_concourse, 'wtr', 'bases/agricultural/Helen_Concourse_wtr'+time_of_day+'.spr', 0, 0.6466)
Base.Texture (room_concourse, 'wk0', 'bases/agricultural/Helen_Concourse_wk0'+time_of_day+'.spr', 0, -0.6466)
Base.Texture (room_concourse, 'wk2', 'bases/agricultural/Helen_Concourse_wk2'+time_of_day+'.spr', 0.185, -0.2507)

# add links between concourse and landing pad
Base.Link (room_landing_pad, 'my_link_id', 0.6025, -0.463333, 0.29, 0.633333, 'Main Concourse', room_concourse)
Base.Link (room_concourse, 'my_link_id', 0.035, -0.346667, 0.2825, 0.27, 'Landing_Pad', room_landing_pad)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)

# add commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room_concourse, 0.6475, -0.366667, 0.32, 0.206667, 'Commodity_Exchange')

# add bar
import bar_lib
bar = bar_lib.MakeBar (room_concourse,time_of_day,'agricultural', "bases/bar/Helen_Bar", True, True, 'agricultural', False, [('ag0', -0.873, -0.1455),('ag1', -0.5638125, -0.1746),('ag2', -0.1151875, -0.1261),('ag3', 0.4061875, -0.0582)])
Base.Link (room_concourse, 'bar', -0.61, -0.113333, 0.2075, 0.25, 'Bar', bar)

# add the guilds
import merchant_guild
if (merchant_guild.Can()):
	merchant = merchant_guild.MakeMerchantGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'merchant', 0.03, 0.0933333, 0.22, 0.176667, "Merchant's Guild", merchant)
else:
	Base.Texture (room_concourse, 'nomerchant', 'bases/agricultural/nomerchant'+time_of_day+'.spr', 0.1455, 0.1552)

import mercenary_guild
if (mercenary_guild.Can()):
	merchant = mercenary_guild.MakeMercenaryGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'mercenary', 0.77, 0.0233333, 0.22, 0.226667, "Mercenary's Guild", merchant)
else:
	Base.Texture (room_concourse, 'nomercenary', 'bases/agricultural/nomercenary'+time_of_day+'.spr', 0.860875, 0.1067)

# add ship dealer
import weapons_lib
weapons_lib.basename="agricultural"
if (weapons_lib.CanRepair()):
	weap = weapons_lib.MakeWeapon (room_concourse,time_of_day)
	Base.Link (room_concourse, 'weapon_room', -0.5725, -0.583333, 0.315, 0.386667, 'Ship_Dealer/Upgrades', weap)
else:
	Base.Texture (room_concourse, 'noshipdealer', 'bases/agricultural/noshipdealer'+time_of_day+'.spr', -0.2606875, -0.4656)

# add mission computer
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room_concourse,time_of_day)
Base.Link (room_concourse, 'my_comp_id', 0.3725, -0.843333, 0.2825, 0.423333, 'Mission_Computer', miscomp)
print ("Linked mission computer")

plist=VS.musicAddList('agricultural.m3u')
VS.musicPlayList(plist)
