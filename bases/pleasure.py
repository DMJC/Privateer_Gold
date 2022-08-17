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
PlayerShip.AddPlayerShips('pleasure',room_landing_pad,'landship')

Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.3125, -0.543333, 0.8975, 0.54, 'Launch')

# add main concourse
room_concourse = Base.Room ('Main_Concourse')
Base.Texture (room_concourse, 'background', 'bases/pleasure/Jolson_Concourse'+time_of_day+'.spr', 0.582, -0.2716)

Base.Texture (room_concourse, 'lts', 'bases/pleasure/Jolson_Concourse_lts'+time_of_day+'.spr', 0, 0)

# link pad and concourse
Base.Link (room_landing_pad, 'my_link_id', 0.66, -0.396667, 0.2425, 0.473333, 'Main_Concourse', room_concourse)
Base.Link (room_concourse, 'my_link_id', 0.6125, -0.713333, 0.2, 0.38, 'Landing_Pad', room_landing_pad)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)

# add bar
import bar_lib
bar = bar_lib.MakeBar (room_concourse,time_of_day,'pleasure','bases/bar/Jolson_Bar',True,True,'pleasure',True,[('pl0',-0.873,-0.1067),('pl1',-0.181875,-0.2522),('pl2',-0.1758125,-0.0485),('pl3',0.351625,-0.0485)])
#Base.Texture(bar,'bartender','bases/pleasure/Jolson_Bar_table.spr',-.75,-.9165)
Base.Link (room_concourse, 'bar', -0.5225, -0.676667, 0.2075, 0.4, 'Bar', bar)

# add commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room_concourse, -0.115, -0.663333, 0.32, 0.51, 'Commodity_Exchange')

# add guilds
import merchant_guild
if (merchant_guild.Can()):
	merchant = merchant_guild.MakeMerchantGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'merchant', 0.3425, -0.666667, 0.0475, 0.326667, 'Merchant_Guild', merchant)
else:
	pass #place blocker
import mercenary_guild
if (mercenary_guild.Can()):
	merchant = mercenary_guild.MakeMercenaryGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'mercenary', 0.2825, -0.666667, 0.045, 0.313333, 'Mercenary_Guild', merchant)
else:
	pass #place blocker

# add ship dealer
import weapons_lib
weapons_lib.basename="pleasure"
if (weapons_lib.CanRepair()):
	weap = weapons_lib.MakeWeapon (room_concourse,time_of_day)
	Base.Link (room_concourse, 'weapon_room', 0.875, -1.0, 0.125, 2.0, 'Ship_Dealer', weap)
else:
	pass #place blocker

# add mission computer
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room_concourse,time_of_day)
Base.Link (room_concourse, 'my_comp_id', 0.415, -0.653333, 0.125, 0.276667, 'Mission_Computer', miscomp)

plist=VS.musicAddList('pleasure.m3u')
VS.musicPlayList(plist)
