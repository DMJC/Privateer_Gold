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
room0 = Base.Room ('Landing_Bay')
Base.Texture (room0, 'lps', 'bases/new_constantinople/NewCon_LandingBay'+time_of_day+'_lps.spr', 0.0788125, 0.0)
Base.Texture (room0, 'background', 'bases/new_constantinople/NewCon_LandingBay'+time_of_day+'.spr', 0, 0)
Base.Texture (room0, 'lgt', 'bases/new_constantinople/NewCon_LandingBay'+time_of_day+'_lgt.spr', -0.5031875, 0.46)
Base.Texture (room0, 'sh0', 'bases/new_constantinople/NewCon_LandingBay'+time_of_day+'_sh0.spr', -0.2954375, 0.4)
Base.Texture (room0, 'sh1', 'bases/new_constantinople/NewCon_LandingBay'+time_of_day+'_sh1.spr', -0.365, 0.54)

PlayerShip.InitPlayerShips()
PlayerShip.AddPlayerShips('new_constantinople',room0,'landship')

Base.LaunchPython (room0, 'my_launch_id', 'bases/launch_hooks.py', -0.515, -0.93, 1.025, 0.94, 'Launch')

# add main concourse
room1 = Base.Room ('Main_Concourse')
Base.Texture (room1, 'stt', 'bases/new_constantinople/NewCon_Concourse'+time_of_day+'_stt.spr', 0, 0.485)		# stars
Base.Texture (room1, 'background', 'bases/new_constantinople/NewCon_Concourse'+time_of_day+'.spr', 0, 0)		# concourse
Base.Texture (room1, 'sh4', 'bases/new_constantinople/NewCon_Concourse'+time_of_day+'_sh4.spr', 0, 0.5)
Base.Texture (room1, 'sh3', 'bases/new_constantinople/NewCon_Concourse'+time_of_day+'_sh3.spr', 0, 0.5)		# ship (Galaxy)
Base.Texture (room1, 'car', 'bases/new_constantinople/NewCon_Concourse'+time_of_day+'_car.spr', 0, 0)
Base.Texture (room1, 'ldp00000', 'bases/new_constantinople/NewCon_Concourse'+time_of_day+'_ldp00000.spr', 0.9154375, 0.3492)

# add link from pad to concourse
Base.Link (room0, 'my_link_id', -0.9475, -0.576667, 0.305, 0.266667, 'Main_Concourse', room1)

# add animated link from concourse to landing pad
Base.Python (room1, 'my_link_id', 0.82, 0.226667, 0.16, 0.746667, 'Hangar', '''#
import Base
Base.EraseObj('''+str(room1)+''',"ldp00000")
Base.Texture ('''+str(room1)+''', "ldp", "bases/new_constantinople/NewCon_Concourse_ldp.spr", 0.9154375, 0.3492)
Base.Python('''+str(room1)+''', "ldp", -1, -1, 2, 2, "Landing_Pad", "#\\n", True)
Base.RunScript('''+str(room1)+''', "trainleave", """#
import Base
Base.SetCurRoom('''+str(room0)+''')
Base.EraseLink('''+str(room1)+''',"ldp")
Base.EraseObj('''+str(room1)+''',"ldp")
Base.EraseObj('''+str(room1)+''',"trainleave")
Base.Texture ('''+str(room1)+''', "ldp00000", "bases/new_constantinople/NewCon_Concourse"+time_of_day+"_ldp00000.spr", 0.9154375, 0.3492)
""", 3.2)
''', False)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room0, room1)


# add commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room1, 0.21, -0.97, 0.755, 0.553333, 'Commodity_Exchange')

#  add bar
import bar_lib
bar = bar_lib.MakeBar (room1,time_of_day,'default','bases/bar/NewCon_Bar', True, True, 'new_constantinople',False,[('nc0', -0.7456875, -0.0194),('nc1',-0.582,-0.1649),('nc2',-0.1394375, -0.1746),('nc3',-0.0909375, -0.1358),('nc4',0.400125, -0.0679)])
Base.Texture (bar, 'beer', 'bases/new_constantinople/beer.spr', 0.36, 0.378)
Base.Link (room1, 'bar', 0.2325, -0.17, 0.0925, 0.176667, 'Bar', bar)

# add guilds
import mercenary_guild
merchant = mercenary_guild.MakeMercenaryGuild (room1,time_of_day)
Base.Link (room1, 'mercenary', -0.0875, -0.266667, 0.23, 0.3, 'Mercenary_Guild', merchant)
import merchant_guild
merchant = merchant_guild.MakeMerchantGuild (room1,time_of_day)
Base.Link (room1, 'merchant', -0.895, -0.423333, 0.5275, 0.483333, 'Merchant_Guild', merchant)

# add mission computer
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room1,time_of_day)
Base.Link (room1, 'my_comp_id', -0.28, -0.306667, 0.14, 0.28, 'Mission_Computer', miscomp)
# print "Linked mission computer"
# print ("Linked mission computer")

# add ship dealer
import weapons_lib
weapons_lib.basename="new_constantinople"
weap = weapons_lib.MakeWeapon (room1,time_of_day, "bases/new_constantinople/nc_shipdealer")
Base.Link (room1, 'weapon_room', 0.515, -0.413333, 0.4575, 0.596667, 'Ship_Dealer/Upgrades', weap)

plist=VS.musicAddList('new_constantinople.m3u')
VS.musicPlayList(plist)
