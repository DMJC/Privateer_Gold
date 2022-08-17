import Base
import dynamic_mission
import VS
import PlayerShip

def MakeIndustrial(sunny,time_of_day='',AWACS=False):

	# this uses the original coordinate system of Privateer
	import GUI
	GUI.GUIInit(320,200,0.03,0.03)

	# add the landing pad
	room_landing_pad = Base.Room ('Landing_Platform')
	if sunny:
		Base.Texture (room_landing_pad, 'background', 'bases/new_detroit/NewDet_LandingPad_Sunny.spr', 0.582, -0.2716)
	else:
		Base.Texture (room_landing_pad, 'background', 'bases/new_detroit/NewDet_LandingPad_BG'+time_of_day+'.spr', 0, 0)
		Base.Texture (room_landing_pad, 'ads', 'bases/new_detroit/NewDet_LandingPad_ads'+time_of_day+'.spr', 0, 0)
		Base.Texture (room_landing_pad, 'background', 'bases/new_detroit/NewDet_LandingPad'+time_of_day+'.spr', 0, 0)
	if (AWACS):
		Base.Texture (room_landing_pad, 'background', 'bases/new_detroit/NewDet_LandingPad_AWACS.spr', 0.582, -0.2716)

	Base.Texture (room_landing_pad, 'rlt', 'bases/new_detroit/NewDet_LandingPad_rlt'+time_of_day+'.spr', 0, 0)
	Base.Texture (room_landing_pad, 'sh0', 'bases/new_detroit/NewDet_LandingPad_sh0'+time_of_day+'.spr', 0, 0.485)
	Base.Texture (room_landing_pad, 'sh1', 'bases/new_detroit/NewDet_LandingPad_sh1'+time_of_day+'.spr', 0.34, 0.55)
	Base.Texture (room_landing_pad, 'sh3', 'bases/new_detroit/NewDet_LandingPad_sh3'+time_of_day+'.spr', 0, 0)
	if not sunny:
		Base.Texture (room_landing_pad, 'rlp', 'bases/new_detroit/NewDet_LandingPad_rlp'+time_of_day+'.spr', 0, 0)

	PlayerShip.InitPlayerShips()
	PlayerShip.AddPlayerShips('new_detroit',room_landing_pad,'landship')

	Base.LaunchPython (room_landing_pad, 'my_launch_id', 'bases/launch_hooks.py', -0.625, -0.193333, 0.595, 0.693333, 'Launch')
	
	# add the main concourse
	room_concourse = Base.Room ('Street_Level')
	
	if sunny:
		Base.Texture (room_concourse, 'background', 'bases/new_detroit/NewDet_Concourse_Sunny.spr', 0.582, -0.2716)
	else:
		Base.Texture (room_concourse, 'background', 'bases/new_detroit/NewDet_Concourse'+time_of_day+'.spr', 0, 0)
	if (AWACS):
		Base.Texture (room_concourse, 'background', 'bases/new_detroit/NewDet_Concourse_AWACS.spr', 0.582, -0.2716)
	if not sunny:
		Base.Texture (room_concourse, 'rcf', 'bases/new_detroit/NewDet_Concourse_rcf'+time_of_day+'.spr', 0, -0.5)
		Base.Texture (room_concourse, 'wk0', 'bases/new_detroit/NewDet_Concourse_wk0'+time_of_day+'.spr', 0, 0)
		Base.Texture (room_concourse, 'hvc', 'bases/new_detroit/NewDet_Concourse_hvc'+time_of_day+'.spr', 0, 0)
		#Base.Texture (room_concourse, 'plc', 'bases/new_detroit/NewDet_Concourse_plc'+time_of_day+'.spr', 0, 0)
		#Base.Texture (room_concourse, 'anc', 'bases/new_detroit/NewDet_Concourse_anc'+time_of_day+'.spr', 0, 0)
		Base.Texture (room_concourse, 'rnc', 'bases/new_detroit/NewDet_Concourse_rnc'+time_of_day+'.spr', 0, 0)
	Base.Texture (room_concourse, 'ber', 'bases/new_detroit/NewDet_Concourse_ber'+time_of_day+'.spr', 0, 0)
	
	# add links between pad and concourse
	Base.Link (room_concourse, 'my_link_id', -0.52, -0.46, 0.08, 0.273333, 'Landing_Platform', room_landing_pad)
	Base.Link (room_landing_pad, 'my_link_id', 0.115, 0.01, 0.585, 0.67, 'Street_Level', room_concourse)
	Base.Link (room_landing_pad, 'my_link_id', -1, -1, 2, 0.2, 'Street_Level', room_concourse)

	# Create the Quine 4000 screens
	import computer_lib
	room_personal_computer = computer_lib.MakePersonalComputer(room_landing_pad, room_concourse)

	# add bar
	import bar_lib
	bar = bar_lib.MakeBar (room_concourse,time_of_day,'industrial','bases/bar/NewDet_Bar', True, True, 'new_detroit', False, [('nd0', -0.691125, 0.0194), ('nd1', -0.3091875, 0.0388), ('nd2', -0.0788125, 0.0485), ('nd3', 0.327375, 0.0776)])
	Base.Link (room_concourse, 'bar', -0.8525, -0.84, 0.2475, 1, 'Bar', bar)

	# add commodity exchange
	import commodity_lib
#	commodity = commodity_lib.MakeCommodity (room_concourse,time_of_day)
#	Base.Link (room_concourse, 'commodity', -0.36, -0.413333, 0.19, 0.176667, 'Commodity_Exchange', commodity)
	commodity_lib.MakeCommodityLink (room_concourse, -0.36, -0.413333, 0.19, 0.176667, 'Commodity_Exchange')

	# add the mission computer
	import mission_computer
	miscomp = mission_computer.MakeMissionComputer (room_concourse,time_of_day,[('background1', 'bases/mission_computer/background_nd.spr', 0.582, -0.2716),('yellowblink', 'bases/mission_computer/yellow_blink.spr', -0.582, 0.8924)])
	Base.Link (room_concourse, 'my_comp_id', 0.785, -0.666667, 0.125, 0.34, 'Mission_Computer', miscomp)

	# add ship dealer
	import weapons_lib
	weapons_lib.basename="new_detroit"
	weap = weapons_lib.MakeWeapon (room_concourse,time_of_day, "bases/new_detroit/nd_shipdealer")
	Base.Link (room_concourse, 'weapon_room', 0.3325, 0.0866667, 0.625, 0.873333, 'Ship_Dealer/Upgrade', weap)
	Base.SetLinkText(weap, 'exit1_to_concourse', "Street_Level")
	Base.SetLinkText(weap, 'exit2_to_concourse', "Street_Level")

	# add the guilds
	import merchant_guild
	merchant = merchant_guild.MakeMerchantGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'merchant', -0.035, -0.0266667, 0.13, 0.236667, 'Merchant_Guild', merchant)
	import mercenary_guild
	merchant = mercenary_guild.MakeMercenaryGuild (room_concourse,time_of_day)
	Base.Link (room_concourse, 'mercenary', -0.04, 0.306667, 0.2325, 0.36, 'Mercenary_Guild', merchant)
