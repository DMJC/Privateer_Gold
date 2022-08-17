import Base
import dynamic_mission
import VS
import quest

time_of_day=''
bar=-1
weap=-1
room0=-1
plist=VS.musicAddList('captured.m3u')
VS.musicPlayList(plist)
room = Base.Room ('Endless Pain?')
room0 = room
Base.Texture (room, 'background', 'bases/generic/airlock.spr', 0, 0)
Base.LaunchPython (room0, 'launch','#\nVS.getPlayer().Kill()', -1,-1,1,1, 'There is an Airlock...')
#Base.Ship (room0, 'ship', (0,-.6,4),(0,.93,-.34) ,(-1,0,0))
import campaign_lib
cnodelist=campaign_lib.getActiveCampaignNodes(room0)
