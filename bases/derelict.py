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

plist=VS.musicAddList('derelict.m3u')
VS.musicPlayList(plist)
dynamic_mission.CreateMissions()

# add landing pad
room_landing_pad = Base.Room ('')
Base.Texture (room_landing_pad, 'sta00', 'bases/derelict/derelict'+time_of_day+'_sta00.spr', 0, 0)
Base.Texture (room_landing_pad, 'background', 'bases/derelict/derelict'+time_of_day+'.spr', 0, 0)

PlayerShip.InitPlayerShips()
PlayerShip.AddPlayerShips('derelict',room_landing_pad,'landship')

Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.53, -0.423333, 0.35, 0.276667, 'Launch')

# add main concourse
room_concourse = Base.Room ('')
Base.Texture (room_concourse, 'sta00', 'bases/derelict/derelict'+time_of_day+'_sta00.spr', 0, 0)
Base.Texture (room_concourse, 'background', 'bases/derelict/derelictship_noweapon'+time_of_day+'.spr', 0, 0)
if not quest.checkSaveValue(VS.getCurrentPlayer(),'have_the_gun'):
	Base.Texture (room_concourse, 'weapon', 'bases/derelict/derelict'+time_of_day+'_sta00.spr', 0, 0)
	Base.Texture (room_concourse, 'weapon', 'bases/derelict/derelictship_weapon'+time_of_day+'.spr', 0, 0)
	Base.Python (room_concourse, 'weapon', -0.605, -0.78, 0.2975, 0.423333, 'Remove Derelict Weapon', '''#
import Base
import VS
plr=VS.getPlayer()
if plr:
	if not quest.checkSaveValue(VS.getCurrentPlayer(),'have_the_gun'):
		if plr.upgrade('steltek_gun',0,0,True,True):
			quest.removeQuest(VS.getCurrentPlayer(),'have_the_gun',1)
			Base.EraseObj('''+str(room_concourse)+''', 'weapon')
			Base.EraseLink('''+str(room_concourse)+''', 'weapon')
	else:
		Base.EraseObj('''+str(room_concourse)+''', 'weapon')
		Base.EraseLink('''+str(room_concourse)+''', 'weapon')
''', False)

# add links between landing pad and concourse
Base.Link (room_landing_pad, 'my_link_id', -0.8225, -0.32, 0.225, 0.2, 'Examine Derelict Fighter', room_concourse)
Base.Link (room_concourse, 'my_link_id', -0.9725, -0.98, 1.945, 0.0766667, 'Back to Your Ship', room_landing_pad)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)
