import Base
import dynamic_mission
import VS

# this uses the original coordinate system of Privateer
import GUI
GUI.GUIInit(320,200,0.03,0.03)

import land_hooks
land_hooks.run()

time_of_day=''
plist=VS.musicAddList('mining_base_pirates.m3u')
VS.musicPlayList(plist)
dynamic_mission.CreateMissions()

# add landing pad
room_landing_pad = Base.Room ('Landing_Pad')
Base.Texture (room_landing_pad, 'background', 'bases/mining_base/MiningBase_LandingPad'+time_of_day+'.spr', 0.582, -0.2716)
Base.Ship (room_landing_pad, 'my_ship', (0.044375,-0.319167,2), (0, 0.93, -0.34), (-1, 0, 0))

Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.5075, -0.58, 0.8025, 0.76, 'Launch')

# add main concourse
room_concourse = Base.Room ('Pirate_Concourse')
Base.Texture (room_concourse, 'background', 'bases/mining_base_pirates/PirateBase_Concourse'+time_of_day+'.spr', 0.582, -0.2716)

# add links between pad and concourse
Base.Link (room_landing_pad, 'my_link_id', 0.5875, -0.36, 0.2975, 0.573333, 'Pirate_Concourse', room_concourse)
#Base.Link (room_concourse, 'my_link_id', -0.9625, -0.976667, 1.92, 0.33, 'Landing_Pad', room_landing_pad)
Base.Link (room_concourse, 'my_link_id', -.5, 0.1, .3, 0.33, 'Landing_Pad', room_landing_pad)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)

# add commodity exchange
import commodity_lib
commodity_lib.MakeCommodityLink (room_concourse, 0.705, -0.62, 0.255, 0.423333, 'Commodity_Exchange')

# add mission computer
#Base.Comp (room_concourse, 'my_comp_id', 0.485, -0.443333, 0.1475, 0.163333, 'Mission_Computer', 'Missions News ShipDealer Info ')
import mission_computer
miscomp = mission_computer.MakeMissionComputer (room_concourse,time_of_day)
Base.Link (room_concourse, 'my_comp_id', 0.4075, -0.85, 0.15, 0.276667, 'Mission_Computer', miscomp)

# add bar
import bar_lib
bar = bar_lib.MakeBar (room_concourse,time_of_day,'pirates','bases/bar/MiningBase_Bar',True,True,'mining_base',False,[('mb1',-0.4546875,-0.2232)])
Base.Link (room_concourse, 'bar', 0.2875, -0.29, 0.205, 0.22, 'Bar', bar)
