import Base
import dynamic_mission
import VS

# this uses the original coordinate system of Privateer
import GUI
GUI.GUIInit(320,200,0.03,0.03)

time_of_day=''
dynamic_mission.CreateMissions()

# add landing pad
import pleasure_land
room0 = pleasure_land.MakePleasureAgriculturalLanding(time_of_day)

# add temple
room = Base.Room ('Temple')
room1 = room
import quest
done_comp=False
if quest.checkSaveValue(VS.getCurrentPlayer(),"jones_dead",1.0):
	Base.Texture (room, 'background', 'bases/church_of_man/GaeaDead.spr', .582, -.2716)
	Base.Texture (room, 'smk', 'bases/church_of_man/smk.spr', .582, -.2716)
	plist=VS.musicAddList('church_of_man_dead.m3u')
	done_comp=True
else:
	Base.Texture (room, 'background', 'bases/church_of_man/Gaea.spr', .582, -.2716)
	Base.Texture (room, 'fr0', 'bases/church_of_man/fr0.spr', -0.6001875, 0.4947)
	Base.Texture (room, 'fr1', 'bases/church_of_man/fr1.spr', 0.666875, 0.6596)
	Base.Texture (room, 'eye', 'bases/church_of_man/eye.spr', 0.0, 0.5335)
	Base.Texture (room, 'lgo', 'bases/church_of_man/lgo.spr', -0.07275, -0.3783)
	Base.Texture (room, 'sn0', 'bases/church_of_man/sn0.spr', -0.582, -0.5238)
	Base.Texture (room, 'sn1', 'bases/church_of_man/sn1.spr', 0.7699375, -0.2619)
	plist=VS.musicAddList('church_of_man.m3u')

# play the appropriate music
VS.musicPlayList(plist)

# add links between pad and temple
Base.Link (room0, 'my_link_id', 0.6025, -0.463333, 0.29, 0.633333, 'Pay_Homage_at_Temple_Gaea', room1)
Base.Link (room1, 'my_link_id', -0.9725, -0.97, 0.3625, 0.213333, 'Back_to_Your_Ship', room0)

# Create the Quine 4000 screens
import computer_lib
room_personal_computer = computer_lib.MakePersonalComputer(room0, room1)

# talk to the church of man worshipper
import campaign_lib
if len(campaign_lib.getActiveCampaignNodes(room1)):
# not needed
#	if not done_comp:
#		done_comp=True
	Base.Python (room1, 'my_link_id', -0.6775, -0.826, 0.47, 0.40, 'Beg_for_forgiveness', '#\nimport campaign_lib\nimport campaign_lib\ncampaign_lib.clickFixer('+str(room1)+')\n',False)
