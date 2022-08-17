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
Base.Texture (room_landing_pad, 'background', 'bases/mining_base/MiningBase_LandingPad'+time_of_day+'.spr', 0, 0)
Base.Texture (room_landing_pad, 'lgt', 'bases/mining_base/MiningBase_LandingPad_lgt'+time_of_day+'.spr', 0.6698, 0.564733333)
Base.Texture (room_landing_pad, 'shp', 'bases/mining_base/MiningBase_LandingPad_shp'+time_of_day+'.spr', 0, 0)

PlayerShip.InitPlayerShips()
PlayerShip.AddPlayerShips('mining_base',room_landing_pad,'landship')

Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.3325, -0.58, 0.875, 0.653333, 'Launch')

# add main concourse
room_concourse = Base.Room ('Main_Concourse')
Base.Texture (room_concourse, 'background', 'bases/mining_base/MiningBase_Concourse'+time_of_day+'.spr', 0, 0)

# add links between concourse and landing pad
Base.Link (room_landing_pad, 'my_link_id', 0.5875, -0.36, 0.2975, 0.573333, 'Main_Concourse', room_concourse)
Base.Link (room_concourse, 'my_link_id', -0.75, -0.11, 0.215, 0.4, 'Landing_Pad', room_landing_pad)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)

# add the commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room_concourse, 0.6975, -0.216667, 0.275, 0.37, 'Commodity_Exchange')

# add the guilds
import mercenary_guild
if (mercenary_guild.Can()):
	room_mercenary = mercenary_guild.MakeMercenaryGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'mercenary', 0.2625, 0.196667, 0.225, 0.203333, 'Mercenary_Guild', room_mercenary)
else:
	Base.Texture(room_concourse,'nomercenary','bases/mining_base/nomercenary.spr', 0.41225, 0.2716)

import merchant_guild
if (merchant_guild.Can()):
	room_merchant = merchant_guild.MakeMerchantGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'merchant', 0.6775, 0.31, 0.295, 0.263333, 'Merchant_Guild', room_merchant)
else:
	Base.Texture(room_concourse,'nomerchant','bases/mining_base/nomerchant.spr', 0.8245, 0.4559)

# add mission computer
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room_concourse,time_of_day)
Base.Link (room_concourse, 'my_comp_id', 0.5425, -0.183333, 0.1075, 0.183333, 'Mission_Computer', miscomp)
#print "Linked mission computer"
print ("Linked mission computer")

# add ship dealer
import weapons_lib
weapons_lib.basename="mining_base"
if (weapons_lib.CanRepair()):
	weap = weapons_lib.MakeWeapon (room_concourse,time_of_day)
	Base.Link (room_concourse, 'weapon_room', -0.0975, -0.0466667, 0.2225, 0.326667, 'Ship_Dealer/Upgrade', weap)
	Base.Texture (room_concourse, 'wk0', 'bases/mining_base/MiningBase_Concourse_wk0'+time_of_day+'.spr', -0.352, -0.03)
	Base.Texture (room_concourse, 'car', 'bases/mining_base/MiningBase_Concourse_car'+time_of_day+'.spr', 0, 0)
else:
	Base.Texture(room_concourse,'noshipdealer','bases/mining_base/noshipdealer.spr', 0.036375, 0.0291)
	Base.Texture(room_concourse,'noshipdealer','bases/mining_base/MiningBase_Concourse_lap.spr', 0, 0)

# add bar
import bar_lib
bar = bar_lib.MakeBar (room_concourse,time_of_day,'mining','bases/bar/MiningBase_Bar',True,True,'mining_base',False,[('mb0',-0.788125,-0.2134),('mb1',-0.4546875,-0.2232),('mb2',-0.18187,-0.0485)])
Base.Link (room_concourse, 'bar', 0.275, -0.133333, 0.2375, 0.233333, 'Bar', bar)

plist=VS.musicAddList('mining_base.m3u')
VS.musicPlayList(plist)
