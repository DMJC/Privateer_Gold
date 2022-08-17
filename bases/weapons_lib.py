import Base
import VS
import PlayerShip
import GUI
import methodtype
import string
import quest

import custom

#
# This first section contains the two functions used by individual bases
#	CanRepair
#		returns True or False whether a given base contains a ship dealer and upgrade bay 
#	MakeWeapon
#		creates the base rooms that make up the ship dealer, upgrade bay, and software booth
#
def CanX(disallowed):
	import universe
	sys = VS.getSystemFile()
	(name,fullname)=universe.getDockedBaseName()
	if sys in disallowed or (sys,name) in disallowed or (sys,fullname) in disallowed or name in disallowed or fullname in disallowed:
		return False
	return True
def CanRepair():
	norepair={
		"Gemini/Aldebran":1,
		"Elysia":1,#auriga
		"Gemini/Capella":1,
		"Romulus":1,#castor
		"Gemini/Delta_Prime":1,
		"Gemini/Eden":1,
		"Oresville":1,#hindsvariablen
		"Charon":1,#hyades
		"Speke":1,#junction
		"Victoria":1,#junction
		"Gemini/KM-252":1,
		"Wickerton":1,#manchester
		"New_Reno":1,#nd-57
		"Glasgow":1,#newcaledonia
		"Edom":1,#newconstantinople
		"Liverpool":1,#newcastle
		"Macabee":1,#nexus
		"Gemini/Pentonville":1,
		"Remus":1,#pollux
		"Saratov":1,#prasepe
		"New_Iberia":1,#pyrenees
		"Mjolnir":1,#ragnarok
		"Trinsic":1,#raxis
		"Kronecker":1,#regallis
		"Siva":1,#rikel
		"Erewhon":1,#shangrila
		"Gemini/Sherwood":1,
		"Gemini/Telar":1,
		"Munchen":1,#tingerhoff
		"Valkyrie":1,#valhalla
		"Rilke":1,#varnus
		"Joplin":1,#xxn1927
		}
	return CanX(norepair)

def MakeWeapon(concourse,timeofdayignored='_day', dealername="bases/repair_upgrade/shipdealer",upgradename='bases/repair_upgrade/shipupgrade',use_ship_320_240_upgrade=True):
	import VS
	VS.AdjustRelation("retro","privateer",-0.05,1.0)
	VS.AdjustRelation("kilrathi","privateer",-0.04,1.0)
	VS.AdjustRelation("pirates","privateer",-0.005,1.0)

	# create the ship dealer screen
	room_ship_dealer = Base.Room ('Ship_Dealer')
	Base.Texture (room_ship_dealer, 'background', dealername+'.spr', 0, 0)
	Base.Texture (room_ship_dealer, 'sd', 'bases/repair_upgrade/sd.spr', 0.044, -.0055)

	# add clickable areas to the ship dealer
	Base.Python (room_ship_dealer, 'my_comp_id', -0.9925, -0.263333, 0.8875, 0.56, 'Purchase Centurion', '#\nimport weapons_lib\nweapons_lib.ShipPurchase(\'centurion\')\n',True)
	Base.Python (room_ship_dealer, 'my_comp_id', -0.6825, -0.973333, 0.77, 0.516667, 'Purchase Orion', '#\nimport weapons_lib\nweapons_lib.ShipPurchase(\'orion\')\n',True)
	Base.Python (room_ship_dealer, 'my_comp_id', 0.2925, -0.96, 0.68, 0.733333, 'Purchase Galaxy', '#\nimport weapons_lib\nweapons_lib.ShipPurchase(\'galaxy\')\n',True)

	# create the repair bay and add a link
	room_repair_bay = MakeRepairBay(room_ship_dealer, upgradename, use_ship_320_240_upgrade)

	# add exits to the concourse
	Base.Link (room_ship_dealer, 'exit1_to_concourse',  -0.27, 0.466667, 0.1725, 0.293333, 'Main_Concourse',concourse)
	Base.Link (room_ship_dealer, 'exit2_to_concourse',  0.415, 0.0533333, 0.3175, 0.24, 'Main_Concourse',concourse)

	# calculate the basic repair cost here, so that it only appears once
	# RepairCost() always returns >= 1; a precentage would be more useful
#	global basic_repair_cost
#	basic_repair_cost = VS.getPlayer().RepairCost()
#	print "::: VS.getPlayer().RepairCost()"
#	print basic_repair_cost

	# return room number, to allow bases to call Base.Link to this room
	return room_ship_dealer

#
# These two functions are called by MakeWeapon; they move code that's 
# unrelated to ship purchasing elsewhere, to make MakeWeapon somewhat simpler
#		MakeRepairBay
#		MakeSoftwareBooth
#
def MakeRepairBay(room_ship_dealer, upgradename, use_ship_320_240_upgrade):
	# create the repair bay screen
	room_repair_bay = Base.Room ('Repair/Upgrade')

	# create the software booth screen
	room_software_booth = MakeSoftwareBooth(room_repair_bay)

	# create the repair bay animation screen
	room_animation = Base.Room ('XXXRepair/Upgrade_Loading')	# create an interstitial screen
	RepairBayComputer.singleton = None
	animation = RepairBayComputerAnimation(room_animation, room_repair_bay, upgradename, use_ship_320_240_upgrade)

	# create link from ship dealer to animation screen
	# this also resets the repair bay and software booth computers
	Base.LinkPython (room_ship_dealer, 'repair_bay_link', """#
import GUI
GUI.GUIRootSingleton.rooms[%s].owner.reset()
GUI.GUIRootSingleton.rooms[%s].owner.reset()
""" %(room_animation, room_software_booth), -0.0175, 0.336667, 0.66, 0.45, 'Repair_and_Upgrade', room_animation)

	# add textures to the repair bay
	x=0
	y=0
	if use_ship_320_240_upgrade:
		x=0.582
		y=-0.2716
	Base.Texture (room_repair_bay, 'background', upgradename+'.spr', x, y)

 	# add ship sprites
	PlayerShip.AddPlayerShips('shipupgrade',room_repair_bay,'repairship')

	# add clickable areas to the repair bay
#	temporary - these two Base.Comp calls will be removed once the repair bay computer is fully functional
#	Base.Comp (room_repair_bay, 'my_comp_id', -0.855, -0.81, 0.6325, 0.663333, 'Upgrade/Repair', 'Upgrade Info ')
	Base.Comp (room_repair_bay, 'my_comp_id', 0.9, -1, 0.1, 2, 'Old Upgrade/Repair Computer', 'Upgrade Info Cargo Missions ')
	(x, y, w, h) = GUI.GUIRect(0, 50, 70, 30).getHotRect()
	Base.Link (room_repair_bay, 'my_link_id', x, y, w, h, 'Ship_Dealer', room_ship_dealer)
	(x, y, w, h) = GUI.GUIRect(132, 35, 53, 43).getHotRect()
	Base.Link (room_repair_bay, 'my_comp_id', x, y, w, h, 'Software_Booth', room_software_booth)

	comp = RepairBayComputer(room_repair_bay)

	return room_repair_bay


def MakeSoftwareBooth(room_repair_bay):
	""" Create the software booth interface screen """
	room_software_booth = Base.Room('Software_Booth')

	# create the software booth computer
	comp = SoftwareBoothComputer(room_software_booth)

	# create link back to repair bay
	Base.Link (room_software_booth, 'link_exit_1', -1, -1, 2, 0.02, 'Exit', room_repair_bay)
	Base.Link (room_software_booth, 'link_exit_2', -1, -0.98, 0.0625, 1.98, 'Exit', room_repair_bay)

	return room_software_booth


#
# These functions are used to direct the actions of button clicks in the Software Booth and 
# 	Repair Bay computers
#
def display_click(self,params):
	GUI.GUIRadioButton.onClick(self,params)
	if self.isEnabled():
		self.room.owner.display(self.index)

def mode_click(self,params):
	# allow disabling of the radio buttons
	if self.room.owner.enabled:
		GUI.GUIRadioButton.onClick(self,params)
		if self.isEnabled():
			self.room.owner.set_state(self.index)

def next_click(self,params):
	GUI.GUIButton.onClick(self,params)
	if self.isEnabled():
		self.room.owner.next()
#		next(self.room.owner)

def prev_click(self,params):
	GUI.GUIButton.onClick(self,params)
	if self.isEnabled():
		self.room.owner.previous()

def select_click(self,params):
	GUI.GUIButton.onClick(self,params)
	if self.isEnabled():
		self.room.owner.select()

def mount_select_click(self,params):
	GUI.GUIRadioButton.onClick(self,params)
	if self.isEnabled():
		self.room.owner.mount_select(self.index)

# 
# A few functions to translate software booth items from their internal representation 
# to a useful format for the user (display name, sprites, radar to button mapping, etc)
#
def lookup_software_name(item_name):
	names = {
		'B_and_S_Tripwire': 'B&S Tripwire', 
		'B_and_S_EYE': 'B&S E.Y.E.', 
		'B_and_S_Omni': 'B&S Omni',
		'hunter_aw_6': 'Hunter AW6',
		'hunter_aw_6i': 'Hunter AW6i',
		'hunter_aw_infinity': 'Hunter AW Infinity',
		'iris_mk1': 'Iris Mk I', 
		'iris_mk2': 'Iris Mk II', 
		'iris_mk3': 'Iris Mk III',
		'humboldt_map': 'Humboldt Quadrant Map', 
		'farris_map': 'Fariss Quadrant Map',
		'potter_map': 'Potter Quadrant Map', 
		'clarke_map': 'Clarke Quadrant Map', 
		'gemini_map': 'All Quadrants'
		}
	try:
		name = names[item_name]
	except:
		name = item_name.title()
	return name

def lookup_software_sprite(item_name):
	sprites = {
		'B_and_S_Tripwire': 'bases/repair_upgrade/items/bandstripwire.spr', 
		'B_and_S_EYE': 'bases/repair_upgrade/items/bandseye.spr', 
		'B_and_S_Omni': 'bases/repair_upgrade/items/bandsomni.spr', 
		'hunter_aw_6': 'bases/repair_upgrade/items/hunteraw6.spr', 
		'hunter_aw_6i': 'bases/repair_upgrade/items/hunteraw6i.spr', 
		'hunter_aw_infinity': 'bases/repair_upgrade/items/hunterawinfinity.spr', 
		'iris_mk1': 'bases/repair_upgrade/items/irismk1.spr', 
		'iris_mk2': 'bases/repair_upgrade/items/irismk2.spr', 
		'iris_mk3': 'bases/repair_upgrade/items/irismk3.spr',
		'humboldt_map': 'bases/repair_upgrade/items/map_humboldt.spr', 
		'farris_map': 'bases/repair_upgrade/items/map_fariss.spr', 
		'potter_map': 'bases/repair_upgrade/items/map_potter.spr', 
		'clarke_map': 'bases/repair_upgrade/items/map_clarke.spr', 
		'gemini_map': 'bases/repair_upgrade/items/map_gemini.spr'
		}
	try:
		sprite = sprites[item_name]
	except:
		# a blank sprite
		sprite = ''
	return sprite

def lookup_software_damaged_sprite(item_name):
	sprites = {
		'B_and_S_Tripwire':		'bases/repair_upgrade/items/damaged/dmg-bandstripwire.spr', 
		'B_and_S_EYE':			'bases/repair_upgrade/items/damaged/dmg-bandseye.spr', 
		'B_and_S_Omni':			'bases/repair_upgrade/items/damaged/dmg-bandsomni.spr', 
		'hunter_aw_6':			'bases/repair_upgrade/items/damaged/dmg-hunteraw6.spr', 
		'hunter_aw_6i':			'bases/repair_upgrade/items/damaged/dmg-hunteraw6i.spr', 
		'hunter_aw_infinity':	'bases/repair_upgrade/items/damaged/dmg-hunterawinfinity.spr', 
		'iris_mk1':				'bases/repair_upgrade/items/damaged/dmg-irismk1.spr', 
		'iris_mk2':				'bases/repair_upgrade/items/damaged/dmg-irismk2.spr', 
		'iris_mk3':				'bases/repair_upgrade/items/damaged/dmg-irismk3.spr'
		}
	try:
		sprite = sprites[item_name]
	except:
		# a blank sprite
		sprite = lookup_software_sprite(item_name)
	return sprite

def lookup_radio_button(item_name):
	radio_buttons = {
		'B_and_S_Tripwire': 'btn_a1', 
		'B_and_S_EYE': 'btn_a2', 
		'B_and_S_Omni': 'btn_a3', 
		'hunter_aw_6': 'btn_b1', 
		'hunter_aw_6i': 'btn_b2', 
		'hunter_aw_infinity': 'btn_b3', 
		'iris_mk1': 'btn_c1', 
		'iris_mk2': 'btn_c2', 
		'iris_mk3': 'btn_c3',
		'humboldt_map': 'btn_map1', 
		'farris_map': 'btn_map2', 
		'potter_map': 'btn_map3', 
		'clarke_map': 'btn_map4', 
		'gemini_map': 'btn_map5'
		}
	try:
		button = radio_buttons[item_name]
	except:
		# an unknown button
		button = ''
	return button

# 
# get the player's currently installed radar
#
def get_current_radar():
	radars = []
	player = VS.getPlayer()

	for i in range(player.numCargo()):
		cargo = player.GetCargoIndex(i)
		category = cargo.GetCategory()
		if not (category[:14] == 'upgrades/Radar' or category[:22] == 'upgrades/Damaged/Radar'): continue
		name = cargo.GetContent()
		try:
#			damage = cargo.GetFunctionality()/cargo.GetMaxFunctionality()
			damage = player.PercentOperational(name, category, False)
		except:
			damage = 1.0
		radars.append( [name, damage] )

	return radars

#
# create sell and repair lists
#
def get_repair_list(radar):
	repair = []
	for i in range(len(radar)):
	# temporarily make the radar damaged
#		radar[i][1] = 0.75
		if (radar[i][1] < 1.0):
			repair.append( i )

#	print "::: get_repair_list [for radar]"
	print ("::: get_repair_list [for radar]")
	import pprint
	pprint.pprint( repair )

	return repair

def get_sell_list():
	sell = get_current_radar()
	cp=VS.getCurrentPlayer()

	if quest.checkSaveValue(cp,'humboldt_map',1):
		sell.append( ['humboldt_map', 1.0] )
	if quest.checkSaveValue(cp,'farris_map',1):
		sell.append( ['farris_map', 1.0] )
	if quest.checkSaveValue(cp,'potter_map',1):
		sell.append( ['potter_map', 1.0] )
	if quest.checkSaveValue(cp,'clarke_map',1):
		sell.append( ['clarke_map', 1.0] )

#	print "::: get_sell_list [for radar]"
	print ("::: get_sell_list [for radar]")
	import pprint
	pprint.pprint( sell )

	return sell

def make_light_spriteset(lit_sprite):
	# minimum spriteset entries for a radio/check button: checked/unchecked/disabled
	return { 'checked':lit_sprite, 'unchecked':None, 'disabled':None }


#
# SoftwareBoothComputerGeneric:
#	server-side version of software booth, contains lists
#
class SoftwareBoothComputerGeneric:
	def __init__(self):
		# farris_map should be fariss_map, but left as is for backwards compatiblity
		self.items = [ 
			'B_and_S_Tripwire', 
			'B_and_S_EYE', 
			'B_and_S_Omni',  
			'hunter_aw_6', 
			'hunter_aw_6i', 
			'hunter_aw_infinity',  
			'iris_mk1', 
			'iris_mk2', 
			'iris_mk3',  
			'humboldt_map', 
			'farris_map', 
			'potter_map', 
			'clarke_map', 
			'gemini_map'	 ]

		# set up buy, sell and repair prices
		self.buy_prices    = {'humboldt_map': 2000, 'farris_map': 2000, 'potter_map': 2000, 'clarke_map': 2000, 'gemini_map': 5000}
		self.sell_prices   = {'humboldt_map': 1000, 'farris_map': 1000, 'potter_map': 1000, 'clarke_map': 1000}
		# maps can't be damaged
		self.repair_prices = {}
		# get list of radar units
		global master_part_list
		radar_list = master_part_list.getRadarList()
		for cargo in radar_list:
			name     = cargo.GetContent()
			try:
				buy_price    = int( cargo.GetPrice() )
				# in the original, the sell price wasn't a set ratio of the buy price, like we're doing here
				sell_price   = int( buy_price * 0.75 )
				repair_price = int( buy_price * 0.45 ) # if the item is 100% damaged, player only has to pay this percent of the purchase price
				self.buy_prices[name]    = buy_price
				self.sell_prices[name]   = sell_price
				self.repair_prices[name] = repair_price
			except:
				pass
		
		self.reset()
	
	def reset(self):
		# also, rebuild the sell/repair lists, in case user sold radar somehow
		self.sell   = get_sell_list()
		self.repair = get_repair_list(self.sell)
	def setstatus(self,success,message):
		self.status = [success and "success" or "failure", message]
	#def draw(self,message=None):
	#	pass
	#def drawBlank(self,message=None):
	#	pass
	def resetstatus(self):
		self.status = ["failure", "Unknown error"]

	def sell_server(self, item_name_sent):
		self.resetstatus()
		item_name=''
		sell_index = 0
		for item_name, undamaged in self.sell:
			if item_name == item_name_sent:
				break
			sell_index += 1
		if item_name != item_name_sent:
			self.setstatus(False, "CAN'T SELL ITEM "+str(item_name_sent))
		else:
			price = int( self.sell_prices[item_name] * undamaged )
			player = VS.getPlayer()
			maps = {'humboldt_map': 1, 'farris_map': 1, 'potter_map': 1, 'clarke_map': 1}
			if item_name in maps:
				# selling a map
				player.addCredits(price)
				remove_map(item_name)
				self.sell.pop(sell_index)
			else:
				# selling a radar
				player.addCredits(price)
				remove_item(player, item_name)
				self.sell.pop(sell_index)
			self.setstatus(True, "Thank You")
		return self.status

	def repair_server(self, item_name_sent):
		self.resetstatus()
		item_name=''
		repair_index = 0
		for item_name, damage in self.sell:
			if item_name == item_name_sent:
				break
			repair_index += 1
		if item_name != item_name_sent:
			self.setstatus(False, "Can't find repair item "+str(item_name_sent))
		elif repair_index not in self.repair:
			self.setstatus(False, "ERROR: "+str(item_name_sent)+" CANNOT BE REPAIRED")
		else:
			# repair cost is the fraction of functionality * the repair_price
			price = int( self.repair_prices[item_name] * (1.0 - damage) )
			player = VS.getPlayer()
			if player.getCredits() < price:
				self.setstatus(False, "INSUFFICIENT CREDIT")
			else:
				# deduct cost, repair item, and update repair list (it should be empty, but maybe there's some wierd condition out there)
				player.addCredits(-1 * price)
				repair_item(player,item_name)
				self.repair.remove(repair_index)
				self.sell[repair_index][1] = 1.0
				self.setstatus(True, "ITEM REPAIRED")
		return self.status

	def buy_server(self, item_name):
		self.resetstatus()
		if item_name not in self.items:
			self.setstatus(False, "UNKNOWN ITEM "+str(item_name))
		else:
			price = self.buy_prices[item_name]
			player = VS.getPlayer()
			maps = {'humboldt_map': 1, 'farris_map': 1, 'potter_map': 1, 'clarke_map': 1}
			if player.getCredits() < price:
				self.setstatus(False, "INSUFFICIENT CREDIT")
			else:
				# player has enough credits to buy item
				if item_name=='gemini_map':
					if has_map('humboldt_map') and has_map('farris_map') and has_map('potter_map') and has_map('clarke_map'):
						self.setstatus(False, "MAP ALREADY LOADED")
					else:
						# buy all 4 quadrant maps
						player.addCredits(-1 * price)
						add_map('humboldt_map')
						add_map('farris_map')
						add_map('potter_map')
						add_map('clarke_map')
						# update the sell and repair lists
						self.sell   = get_sell_list()
						self.repair = get_repair_list(self.sell)
						self.setstatus(True, "Thank You")
				elif item_name in maps:
					if has_map(item_name):
						self.setstatus(False, "MAP ALREADY LOADED")
					else:
						# buy an individual map
						player.addCredits(-1 * price)
						add_map(item_name)
						# update the sell and repair lists
						self.sell   = get_sell_list()
						self.repair = get_repair_list(self.sell)
						self.setstatus(True, "Thank You")
				else:
					if len(get_current_radar()) > 0:
						self.setstatus(False, "NO ROOM ON SHIP")
					else:
						# buy a radar unit
						player.addCredits(-1 * price)
						add_item(player, item_name, price)
						# update the sell and repair lists
						self.sell   = get_sell_list()
						self.repair = get_repair_list(self.sell)
						self.setstatus(True, "Thank You")
		return self.status

	def handle_server_cmd(self, args):
		cmd = args[0]
		if cmd == "buy":
			return self.buy_server(args[1])
		elif cmd == "sell":
			return self.sell_server(args[1])
		elif cmd == "repair":
			return self.repair_server(args[1])
		elif cmd == "reload":
			self.reset()
			return ["success", "Reloaded"]
		else:
			return ["failure", "Error: subcommand %s not valid" % args[0]]

#
# SoftwareBoothComputer
#	displays upgrade options for ship radars and sector/quadrant nav maps
#	handles buy/sell/repair code
#
class SoftwareBoothComputer (SoftwareBoothComputerGeneric):
	singleton = None
	def __init__(self,room_software_booth):
		self.room_id  = room_software_booth

		SoftwareBoothComputer.singleton = self

		# initial state is "buy"
		self.state = "buy"
		self.enabled = 1
		self.current_item = 0
		guiroom = GUI.GUIRoom(room_software_booth)
		self.guiroom = guiroom

		# when a button is clicked, this will allow us to get the SoftwareBoothComputer instance from the x_click functions
		guiroom.owner = self
		
		# main sprite - this doesn't change, so we don't need to keep a variable for it
		GUI.GUIStaticImage(guiroom, 'background', ( 'bases/repair_upgrade/software.spr', GUI.GUIRect(0, 0, 320, 200) ))
	
		self.buttons = {}

		# main buttons
		sprite_repair_checked = ('bases/repair_upgrade/buttons/repair_pressed.spr'   , GUI.GUIRect(85 ,168,39,28,"pixel",(512,512)))
		sprite_buy_checked    = ('bases/repair_upgrade/buttons/buy_pressed.spr'      , GUI.GUIRect(32 ,432,36,46,"pixel",(512,512)))
		sprite_sell_checked   = ('bases/repair_upgrade/buttons/sell_pressed.spr'     , GUI.GUIRect(72 ,432,36,46,"pixel",(512,512)))
		sprite_prev_checked   = ('bases/repair_upgrade/buttons/prev_item_pressed.spr', GUI.GUIRect(117,438,28,35,"pixel",(512,512)))
		sprite_next_checked   = ('bases/repair_upgrade/buttons/next_item_pressed.spr', GUI.GUIRect(146,438,28,35,"pixel",(512,512)))
		repair_sprset         = {'checked':sprite_repair_checked, 'unchecked':None, 'down':sprite_repair_checked}
		buy_sprset            = {'checked':sprite_buy_checked   , 'unchecked':None, 'down':sprite_buy_checked}
		sell_sprset           = {'checked':sprite_sell_checked  , 'unchecked':None, 'down':sprite_sell_checked}
		prev_sprset           = {'down':sprite_prev_checked, 'enabled':None, 'disabled':None}
		next_sprset           = {'down':sprite_next_checked, 'enabled':None, 'disabled':None}
		self.add_button( GUI.GUIButton     (guiroom, 'Select Item',   'btn_select', {}           , GUI.GUIRect(19,  91, 94, 69)                       ), select_click )
		self.add_button( GUI.GUIRadioButton(guiroom, 'Repair Mode',   'btn_repair', repair_sprset, GUI.GUIRect(50,  66, 30, 10), 'software_booth_mode'), mode_click )
		self.add_button( GUI.GUIRadioButton(guiroom, 'Buy Mode',      'btn_buy',    buy_sprset   , GUI.GUIRect(22, 170, 18, 15), 'software_booth_mode'), mode_click )
		self.add_button( GUI.GUIRadioButton(guiroom, 'Sell Mode',     'btn_sell',   sell_sprset  , GUI.GUIRect(47, 170, 19, 15), 'software_booth_mode'), mode_click )
		self.add_button( GUI.GUIButton     (guiroom, 'Previous Item', 'btn_prev',   prev_sprset  , GUI.GUIRect(75, 172, 14, 12)                       ), prev_click )
		self.add_button( GUI.GUIButton     (guiroom, 'Next Item',     'btn_next',   next_sprset  , GUI.GUIRect(94, 172, 13, 12)                       ), next_click )

		# set buy mode radio group
		GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index,'check',{'index':'btn_buy'})

		# map buttons
		sprite_map1 = ('bases/repair_upgrade/buttons/green_light.spr', GUI.GUIRect( 68,123,13,15,"pixel",(512,512)))
		sprite_map2 = ('bases/repair_upgrade/buttons/green_light.spr', GUI.GUIRect(167,123,13,15,"pixel",(512,512)))
		sprite_map3 = ('bases/repair_upgrade/buttons/green_light.spr', GUI.GUIRect(263,123,13,15,"pixel",(512,512)))
		sprite_map4 = ('bases/repair_upgrade/buttons/green_light.spr', GUI.GUIRect(362,123,13,15,"pixel",(512,512)))
		sprite_map5 = ('bases/repair_upgrade/buttons/green_light.spr', GUI.GUIRect(461,123,13,15,"pixel",(512,512)))
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Humboldt Quadrant Map', 'btn_map1', make_light_spriteset(sprite_map1), GUI.GUIRect( 16, 8, 42, 35), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Fariss Quadrant Map',   'btn_map2', make_light_spriteset(sprite_map2), GUI.GUIRect( 76, 8, 44, 35), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Potter Quadrant Map',   'btn_map3', make_light_spriteset(sprite_map3), GUI.GUIRect(137, 8, 44, 35), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Clarke Quadrant Map',   'btn_map4', make_light_spriteset(sprite_map4), GUI.GUIRect(199, 8, 44, 35), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Gemini Sector Map',     'btn_map5', make_light_spriteset(sprite_map5), GUI.GUIRect(260, 8, 44, 35), 'software_booth_display'), display_click )

		# radar buttons
		sprite_a1 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(291,255,9,13,"pixel",(512,512)))
		sprite_a2 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(387,254,9,13,"pixel",(512,512)))
		sprite_a3 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(483,254,9,13,"pixel",(512,512)))
		sprite_b1 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(293,377,9,13,"pixel",(512,512)))
		sprite_b2 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(387,378,9,13,"pixel",(512,512)))
		sprite_b3 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(482,377,9,13,"pixel",(512,512)))
		sprite_c1 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(293,500,9,13,"pixel",(512,512)))
		sprite_c2 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(387,500,9,13,"pixel",(512,512)))
		sprite_c3 = ('bases/repair_upgrade/buttons/red_light.spr', GUI.GUIRect(481,500,9,13,"pixel",(512,512)))
		self.add_button( GUI.GUIRadioButton(guiroom,'Display B and S Tripwire',   'btn_a1', make_light_spriteset(sprite_a1), GUI.GUIRect(136,  61, 51, 41), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display B and S E.Y.E.',     'btn_a2', make_light_spriteset(sprite_a2), GUI.GUIRect(195,  61, 51, 41), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display B and S Omniscience','btn_a3', make_light_spriteset(sprite_a3), GUI.GUIRect(254,  61, 51, 41), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Hunter AW-6',        'btn_b1', make_light_spriteset(sprite_b1), GUI.GUIRect(136, 109, 51, 41), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Hunter AW-6i',       'btn_b2', make_light_spriteset(sprite_b2), GUI.GUIRect(195, 109, 51, 41), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Hunter AW Infinity', 'btn_b3', make_light_spriteset(sprite_b3), GUI.GUIRect(254, 109, 51, 41), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Iris Mk. I',         'btn_c1', make_light_spriteset(sprite_c1), GUI.GUIRect(136, 157, 51, 40), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Iris Mk. II',        'btn_c2', make_light_spriteset(sprite_c2), GUI.GUIRect(195, 157, 51, 40), 'software_booth_display'), display_click )
		self.add_button( GUI.GUIRadioButton(guiroom,'Display Iris Mk. III',       'btn_c3', make_light_spriteset(sprite_c3), GUI.GUIRect(254, 157, 51, 40), 'software_booth_display'), display_click )

		# add the text labels
		# select box: GUI.GUIRect(19,  91, 94, 69))  
		# add 5px margin on X value
		txt_color = GUI.GUIColor(0.7,0.7,0.7)
		txt_warning_color = GUI.GUIColor(0.7,0,0)
		self.txt_name    = GUI.GUIStaticText(guiroom,'txt_name',    '', GUI.GUIRect(24,  87, 90, 10), txt_color)
		self.txt_mode    = GUI.GUIStaticText(guiroom,'txt_mode',    '', GUI.GUIRect(24, 154, 60, 10), txt_color)
		self.txt_cost    = GUI.GUIStaticText(guiroom,'txt_cost',    '', GUI.GUIRect(85, 154, 30, 10), txt_color)
		self.txt_credits = GUI.GUIStaticText(guiroom,'txt_credits', '', GUI.GUIRect(24, 149, 90, 10), txt_color)
		self.txt_message = GUI.GUIStaticText(guiroom,'txt_message', '', GUI.GUIRect(24,  92, 90, 10), txt_warning_color)

		# add the item sprite
		self.img_item_rect = GUI.GUIRect(19, 87, 94, 73)
		self.img_item  = GUI.GUIStaticImage(guiroom, 'img_item', None)

		# build item lists
		SoftwareBoothComputerGeneric.__init__(self)

		# draw now
		GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index, 'draw', None)



	def add_button(self, guibutton, onclick_handler):
		# add the button to the "buttons" dictionary, and add onclick handler
		self.buttons[guibutton.index] = guibutton
		guibutton.onClick = methodtype.methodtype(onclick_handler, guibutton, type(guibutton))

	def reset(self):
		# reset computer to initial state
		self.state = "buy"
		self.current_item = 0
		GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'check',{'index':'btn_buy'})

		if VS.networked():
			custom.run("RepairBayComputer", ["reload"], None)
		
		# also, rebuild the sell/repair lists, in case user sold radar somehow
		SoftwareBoothComputerGeneric.reset(self)

		self.draw()
		self.guiroom.redrawIfNeeded()

#	def next(self):
	def __next__(self):
		if self.state=="buy":
			max = len(self.items)
			if max > 0:
				self.current_item = (self.current_item + 1) % max
			else:
				self.current_item = 0

		elif self.state=="sell":
			max = len(self.sell)
			if max > 0:
				self.current_item = (self.current_item + 1) % max
			else:
				self.current_item = 0
		elif self.state=="repair":
			max = len(self.repair)
			if max > 0:
				self.current_item = (self.current_item + 1) % max
			else:
				self.current_item = 0
		self.draw()

	def previous(self):
		if self.state=="buy":
			max = len(self.items) - 1
			self.current_item = self.current_item - 1
			if (self.current_item < 0):
				self.current_item = max

		elif self.state=="sell":
			max = len(self.sell) - 1
			self.current_item = self.current_item - 1
			if (self.current_item < 0):
				self.current_item = max
		elif self.state=="repair":
			max = len(self.repair) - 1
			self.current_item = self.current_item - 1
			if (self.current_item < 0):
				self.current_item = max
		self.draw()

	def select(self):
		"""
			error messages (from SOFTTXT.iff) are:
			Price: 
			Mode:
			Thank You
			INSUFFICIENT CREDIT
			BUY 
			SELL 
			REPR 
			NO ROOM FOR ITEM
			NOT VALID
			NOTHING TO SELL
			NOTHING TO REPAIR
			ITEM REPAIRED
			Credits: 
		"""
		if self.state == "repair":
			if len(self.repair) > 0:
				repair_index = self.repair[self.current_item]
				item_name, damage = self.sell[repair_index]
				# repair cost is the fraction of functionality * the repair_price
				price = int( self.repair_prices[item_name] * (1.0 - damage) )
				player = VS.getPlayer()
				if player.getCredits() < price:
					self.draw("INSUFFICIENT CREDIT")
				else:
					def repairSuccess(args):
						if (args[0] != "success"):
							self.draw(args[1])
							return
						if VS.networked():
							self.repair.pop(self.current_item)
							self.sell[repair_index][1] = 1.0
						if self.current_item > 0:
							self.current_item = self.current_item - 1
						self.drawBlank(args[1])
					custom.run("SoftwareBoothComputer", ["repair", item_name], repairSuccess)

		elif self.state == "sell":
			if len(self.sell) > 0:
				# if there is stuff to sell
				item_name, undamaged = self.sell[self.current_item]
				def sellSuccess(args):
					if (args[0] != "success"):
						self.draw(args[1])
						return
					if VS.networked():
						self.sell.pop(self.current_item)
					if self.current_item > 0:
						self.current_item = self.current_item - 1
					self.drawBlank(args[1])
				custom.run("SoftwareBoothComputer", ["sell", item_name], sellSuccess)

		elif self.state == "buy":
			item_name = self.items[self.current_item]
			price = self.buy_prices[item_name]
			player = VS.getPlayer()
			maps = {'humboldt_map': 1, 'farris_map': 1, 'potter_map': 1, 'clarke_map': 1}
			if player.getCredits() < price:
				self.draw("INSUFFICIENT CREDIT")
			else:
				# player has enough credits to buy item
				def buySuccess(args):
					if args[0] != "success":
						self.draw(args[1])
						return
					if VS.networked():
						# update the sell and repair lists
						self.sell   = get_sell_list()
						self.repair = get_repair_list(self.sell)
					self.draw(args[1])
				custom.run("SoftwareBoothComputer", ["buy", item_name], buySuccess)


	def display(self, button_index):
		if self.state == "buy":
			if   button_index == 'btn_a1': self.current_item = 0
			elif button_index == 'btn_a2': self.current_item = 1
			elif button_index == 'btn_a3': self.current_item = 2
			elif button_index == 'btn_b1': self.current_item = 3
			elif button_index == 'btn_b2': self.current_item = 4
			elif button_index == 'btn_b3': self.current_item = 5
			elif button_index == 'btn_c1': self.current_item = 6
			elif button_index == 'btn_c2': self.current_item = 7
			elif button_index == 'btn_c3': self.current_item = 8
			elif button_index == 'btn_map1': self.current_item = 9
			elif button_index == 'btn_map2': self.current_item = 10
			elif button_index == 'btn_map3': self.current_item = 11
			elif button_index == 'btn_map4': self.current_item = 12
			elif button_index == 'btn_map5': self.current_item = 13
			# else: error
			self.draw()

	def set_state(self, button_index):
		if button_index == "btn_buy":
			if self.state != "buy":
				self.state = "buy"
				self.current_item = 0
				self.draw()
		elif button_index == "btn_sell":
			if self.state != "sell":
				self.state = "sell"
				self.current_item = 0
				self.draw()
		elif button_index == "btn_repair":
			if self.state != "repair":
				self.state = "repair"
				self.current_item = 0
				self.draw()
		# else: state is unknown

	def drawItem(self,item_name,price,message):
		if (type(item_name)==tuple) or (type(item_name)==list):
			item_name,damage = item_name
		else:
			item_name,damage = (item_name,1.0)
		display_name = lookup_software_name(item_name)
		if damage < 1.0:
			sprite       = lookup_software_damaged_sprite(item_name)
		else:
			sprite       = lookup_software_sprite(item_name)
		self.drawItemDetail(sprite, display_name, price, VS.getPlayer().getCredits(), item_name, message)

	def setActiveSelectors(self):
		if self.state == "buy":
			# enable all radio buttons
			GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'enable',{ 'group':'software_booth_display' })
		elif self.state == "sell":
			# disable all
			GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'disable',{ 'group':'software_booth_display' })
			
			# activate one by one those available
			for item in self.sell:
				item_name = item[0]
				radio_button_name = lookup_radio_button(item_name)
				if radio_button_name != '':
					self.buttons[radio_button_name].enable()			

		elif self.state == "repair":
			# disable all
			GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'disable',{ 'group':'software_booth_display' })
			
			# activate one by one those available
			for item in self.repair:
				item_name = self.sell[item]
				radio_button_name = lookup_radio_button(item_name)
				if radio_button_name != '':
					self.buttons[radio_button_name].enable()			


	def draw(self,message=None):
		if self.state == "buy":
			item_name = self.items[self.current_item]
			self.setActiveSelectors();
			self.drawItem(item_name, self.buy_prices[item_name], message)

		elif self.state == "sell":
			self.setActiveSelectors()
			if len(self.sell):
				item_name,damage = self.sell[self.current_item]
				price = int( self.sell_prices[item_name] * damage )
				self.drawItem(item_name, price, message)
			else:
				self.drawBlank("NOTHING TO SELL")

		elif self.state == "repair":
			self.setActiveSelectors()
			if len(self.repair):
				# repair cost is the fraction of functionality * the repair_price
				repair_index = self.repair[self.current_item]
				item_name, damage = self.sell[repair_index]
				price = int( self.repair_prices[item_name] * (1.0 - damage) )
				self.drawItem(item_name, price, message)
			else:
				self.drawBlank("NOTHING TO REPAIR")

	def drawItemDetail(self, spr_file, name, cost, credits, item_name, message=None):
		radio_button_name = lookup_radio_button(item_name)
		if radio_button_name != '':
			self.buttons[radio_button_name].check()
		self.txt_name.setText( name )
#		self.txt_mode.setText( "Mode: %s" %(string.upper(self.state)) )
		self.txt_mode.setText( "Mode: %s" %(self.state.upper()) )
		self.txt_cost.setText( "%s" %(cost) )
		self.txt_credits.setText( "Credits: %s" %(int(credits)) )
		if (spr_file == ''):
			self.img_item.hide()
		else:
			self.img_item.setSprite( (spr_file, self.img_item_rect) )
			self.img_item.show()
		if message==None:
			self.txt_message.setText("")
		else:
			self.txt_message.setText(message)

	def drawBlank(self,message=None):
		GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'uncheck',{ 'group':'software_booth_display' })
		self.txt_name.setText("")
		self.txt_mode.setText("")
		self.txt_cost.setText("")
		self.txt_credits.setText("")
		self.img_item.hide()
		if message==None:
			self.txt_message.setText("")
		else:
			self.txt_message.setText(message)

def handle_SoftwareBoothComputer_message(local, cmd, args, id):
	cp = VS.getCurrentPlayer()
	if VS.isserver():
		import server
		player = server.getDirector().getPlayer(cp)
		if not player.software_booth_computer:
			player.software_booth_computer = SoftwareBoothComputerGeneric()
			if args[0] == "reload":
				return ["success", "loaded"]
		return player.software_booth_computer.handle_server_cmd(args)
	elif SoftwareBoothComputer.singleton:
		return SoftwareBoothComputer.singleton.handle_server_cmd(args)
	else:
#		print "SoftwareBoothComputer has no singleton!"
		print ("SoftwareBoothComputer has no singleton!")
	return ["failure", 'SoftwareBoothComputer has no singleton!']

custom.add("SoftwareBoothComputer", handle_SoftwareBoothComputer_message)

# 
# A few functions to translate repair bay items from their internal representation 
# to a useful format for the user (display name, sprites, etc)
#
def lookup_upgrade_name(item_name):
	names = {
		'shield_4_Level1':		'Shield - Level 1',
		'shield_4_Level2':		'Shield - Level 2',
		'shield_4_Level3':		'Shield - Level 3',
		'shield_4_Level4':		'Shield - Level 4',
		'shield_4_Level5':		'Shield - Level 5',
		'shield_4_Level6':		'Shield - Level 6',
		'shield_4_Level7':		'Shield - Level 7',
		'reactor_level_1':		'Engine - Level 1',
		'reactor_level_2':		'Engine - Level 2',
		'reactor_level_3':		'Engine - Level 3',
		'reactor_level_4':		'Engine - Level 4',
		'reactor_level_5':		'Engine - Level 5',
		'reactor_level_6':		'Engine - Level 6',
		'reactor_level_7':		'Engine - Level 7',
		'ion':					'Ion Pulse Cannon',
		'add_cargo_expansion':		'Cargo Expansion',
		'add_cargo_volume':		'Tarsus Cargo Expansion',
		'add_cargo_volume_galaxy':		'Galaxy Cargo Expansion',
		'medium_turret_meson':			'Turret, Top',
		'medium_turret_rear_meson':		'Turret, Tail',
		'medium_turret_bottom_meson':	'Turret, Bottom',
		'mult_speed_enhancer':			'Speed Enhancer',
		'mult_thrust_enhancer':			'Thrust Enhancer',
		'mult_shield_regenerator':		'Shield Regenerator',
		'plasteel':				'Plasteel Armor',
		'tungsten':				'Tungsten Armor',
		'isometal':				'Isometal Armor',
		'ecm_package_1':		'ECM - Level 1',
		'ecm_package_2':		'ECM - Level 2',
		'ecm_package_3':		'ECM - Level 3',
	}
	try:
		name = names[item_name]
	except:
		name = item_name.title()
	return name

def lookup_item_name(weapon_name):
	# this is needed since the gun names in weapons.xml and master_part_list.csv
	# to even further confuse things, turret names come from units.csv
	names = {
		'laser':			'laser',
		'massdriver':		'mass_driver',
		'meson':			'meson_blaster',
		'neutron':			'neutron_gun',
		'particle':			'particle_cannon',
		'tachyon':			'tachyon_cannon',
		'ion':				'ion',
		'plasma':			'plasma_gun',
		'fusion':			'fusion_gun',
		'steltek':			'steltek_gun',
		'boostedsteltek':	'steltek_gun_boosted',
		'tractor':			'tractor_beam',
		'dumbfire':			'dumbfire_ammo',
		'heatseeker':		'heatseeker_ammo',
		'imagerecognition':	'image_recognition_ammo',
		'friendorfoe':		'friend_or_foe_ammo',
		'protontorpedo':	'proton_torpedo_ammo',

		'turret_medium_meson':			'medium_turret_meson',
		'turret_mediumrear_meson':		'medium_turret_rear_meson',
		'turret_mediumbottom_meson':	'medium_turret_bottom_meson'	# doesn't exist in units.csv, uses 'turret_medium_meson' as well
	}
	try:
		name = names[weapon_name.lower()]
	except:
		name = weapon_name.lower()
	return name

def lookup_weapon_name(item_name):
	# translate name back from master_part_list.csv to weapons.xml
	names = {
		'laser':			'Laser',
		'mass_driver':		'MassDriver',
		'meson_blaster':	'Meson',
		'neutron_gun':		'Neutron',
		'particle_cannon':	'Particle',
		'tachyon_cannon':	'Tachyon',
		'ion':				'Ion',
		'plasma_gun':		'Plasma',
		'fusion_gun':		'Fusion',
		'steltek_gun':		'Steltek',
		'steltek_gun_boosted':	'BoostedSteltek',
		'tractor_beam':		'Tractor',
		'dumbfire_ammo':			'Dumbfire',
		'heatseeker_ammo':			'HeatSeeker',
		'image_recognition_ammo':	'ImageRecognition',
		'friend_or_foe_ammo':		'FriendOrFoe',
		'proton_torpedo_ammo':		'ProtonTorpedo',
	}
	try:
		name = names[item_name.lower()]
	except:
		name = item_name.lower()
	return name

def lookup_upgrade_sprite(item_name):
	# note: *** means item is missing from master_parts_list.csv
	sprites = {
		# shields
		'shield_4_Level1':		'bases/repair_upgrade/items/shield1.spr',
		'shield_4_Level2':		'bases/repair_upgrade/items/shield2.spr',
		'shield_4_Level3':		'bases/repair_upgrade/items/shield3.spr',
		'shield_4_Level4':		'bases/repair_upgrade/items/shield4.spr',		# ***
		'shield_4_Level5':		'bases/repair_upgrade/items/shield5.spr',
		'shield_4_Level6':		'bases/repair_upgrade/items/shield6.spr',		# ***
		'shield_4_Level7':		'bases/repair_upgrade/items/shield7.spr',		# ***
		# engines
		'reactor_level_1':		'bases/repair_upgrade/items/engine1.spr',
		'reactor_level_2':		'bases/repair_upgrade/items/engine2.spr',
		'reactor_level_3':		'bases/repair_upgrade/items/engine3.spr',
		'reactor_level_4':		'bases/repair_upgrade/items/engine4.spr',		# ***
		'reactor_level_5':		'bases/repair_upgrade/items/engine5.spr',
		'reactor_level_6':		'bases/repair_upgrade/items/engine6.spr',		# ***
		'reactor_level_7':		'bases/repair_upgrade/items/engine7.spr',		# ***
		# guns
		'laser':			'bases/repair_upgrade/items/laser.spr',
		'mass_driver':		'bases/repair_upgrade/items/massdriver.spr',
		'meson_blaster':	'bases/repair_upgrade/items/meson.spr',
		'neutron_gun':		'bases/repair_upgrade/items/neutron.spr',
		'particle_cannon':	'bases/repair_upgrade/items/particle.spr',
		'tachyon_cannon':	'bases/repair_upgrade/items/tachyon.spr',
		'ion':				'bases/repair_upgrade/items/ion.spr',
		'plasma_gun':		'bases/repair_upgrade/items/plasma.spr',
		'fusion_gun':		'bases/repair_upgrade/items/fusion.spr',			# ***
		'steltek_gun':		'bases/repair_upgrade/items/steltek.spr',			# ***
		'steltek_gun_boosted':		'bases/repair_upgrade/items/steltek.spr',			# ***
		# missles
		'missile_launcher':			'bases/repair_upgrade/items/missile_launcher.spr',
		'dumbfire_ammo':			'bases/repair_upgrade/items/dumbfire.spr',
		'heatseeker_ammo':			'bases/repair_upgrade/items/heat_seeker.spr',
		'image_recognition_ammo':	'bases/repair_upgrade/items/image_recognition.spr',
		'friend_or_foe_ammo':		'bases/repair_upgrade/items/friend_or_foe.spr',
		# torpedos
		'torpedo_launcher':			'bases/repair_upgrade/items/torpedo_launcher.spr',
		'proton_torpedo_ammo':		'bases/repair_upgrade/items/proton_torpedo.spr',
		# armor
		'basic_armor':		'',
		'plasteel':		'bases/repair_upgrade/items/plasteel.spr',
		'tungsten':		'bases/repair_upgrade/items/tungsten.spr',
		'isometal':		'bases/repair_upgrade/items/isometal.spr',
		'add_ablative_hull_coating':		'bases/repair_upgrade/items/isometal.spr',
		'add_sublimative_hull_coating':		'bases/repair_upgrade/items/isometal.spr',
		# add-ons
		'afterburner':			'bases/repair_upgrade/items/afterburner.spr',
		'add_cargo_expansion':		'bases/repair_upgrade/items/cargo_expansion.spr',
		'add_cargo_volume':		'bases/repair_upgrade/items/cargo_expansion.spr',
		'add_cargo_volume_galaxy':		'bases/repair_upgrade/items/cargo_expansion.spr',
		'ecm_package_1':		'bases/repair_upgrade/items/ecm1.spr',
		'ecm_package_2':		'bases/repair_upgrade/items/ecm2.spr',
		'ecm_package_3':		'bases/repair_upgrade/items/ecm3.spr',
		'jump_drive':			'bases/repair_upgrade/items/jumpdrive.spr',
		'repair_droid':			'bases/repair_upgrade/items/repair_droid.spr',
		'repair_droid_advanced':		'bases/repair_upgrade/items/advanced_repair_droid.spr',
		'tractor_beam':					'bases/repair_upgrade/items/tractor.spr',
		'medium_turret_meson':			'bases/repair_upgrade/items/turret_top.spr',
		'medium_turret_rear_meson':		'bases/repair_upgrade/items/turret_rear.spr',
		'medium_turret_bottom_meson':	'bases/repair_upgrade/items/turret_bottom.spr',
		# rf add-ons
		'gun_cooler':		'bases/repair_upgrade/items/gun_cooler.spr',			# ***
		'mult_speed_enhancer':		'bases/repair_upgrade/items/speedenhancer.spr',		# ***
		'mult_thrust_enhancer':		'bases/repair_upgrade/items/thrustenhancer.spr',
		'mult_shield_regenerator':		'bases/repair_upgrade/items/shield_regenerator.spr',		# ***
		# basic repair
#		'basic_inspection':		'bases/repair_upgrade/items/maneuvering_jets.spr',
		}
	try:
		sprite = sprites[item_name]
	except:
		# a blank sprite
		sprite = 'interfaces/commodity/cargo/default.spr'
	return sprite

def lookup_upgrade_class(item_name):
	"""  a ship is only allowed to install one upgrade for each of the following classes in this list. 	"""
	categories = {
		# shields
		'shield_4_Level1':		'shield',
		'shield_4_Level2':		'shield',
		'shield_4_Level3':		'shield',
		'shield_4_Level4':		'shield',		# ***
		'shield_4_Level5':		'shield',
		'shield_4_Level6':		'shield',		# ***
		'shield_4_Level7':		'shield',		# ***
		# engines
		'reactor_level_1':		'engine',
		'reactor_level_2':		'engine',
		'reactor_level_3':		'engine',
		'reactor_level_4':		'engine',		# ***
		'reactor_level_5':		'engine',
		'reactor_level_6':		'engine',		# ***
		'reactor_level_7':		'engine',		# ***
		# armor
		'plasteel':				'armor',
		'tungsten':				'armor',
		'isometal':				'armor',
		# add-ons
		'ecm_package_1':		'ecm',
		'ecm_package_2':		'ecm',
		'ecm_package_3':		'ecm',
		'repair_droid':				'repair_droid',
		'repair_droid_advanced':	'repair_droid',
		}
	try:
		category = categories[item_name]
	except:
		# a blank sprite
		category = item_name
	return category

def lookup_upgrade_type(item_name):
	# note: *** means item is missing from master_parts_list.csv
	types = {
		# guns
		'laser':					'weapon',
		'mass_driver':				'weapon',
		'meson_blaster':			'weapon',
		'neutron_gun':				'weapon',
		'particle_cannon':			'weapon',
		'tachyon_cannon':			'weapon',
		'ion':						'weapon',
		'plasma_gun':				'weapon',
		'fusion_gun':				'weapon',
		# missles
		'missile_launcher':			'launcher',
		'dumbfire_ammo':			'missile',
		'heatseeker_ammo':			'missile',
		'image_recognition_ammo':	'missile',
		'friend_or_foe_ammo':		'missile',
		# torpedos
		'torpedo_launcher':			'launcher',
		'proton_torpedo_ammo':		'torpedo',
		# turrets
		'medium_turret_meson':			'subunit',
		'medium_turret_rear_meson':		'subunit',
		'medium_turret_bottom_meson':	'subunit',
		# tractor beam 
		'tractor_beam':				'tractor',
		}
	try:
		type = types[item_name]
	except:
		# a blank sprite
		type = 'cargo'
	return type

def lookup_upgrade_damaged_sprite(item_name):
	sprites = {
		# armor
		'plasteel':		'bases/repair_upgrade/items/damaged/plasteel.spr',
		'tungsten':		'bases/repair_upgrade/items/damaged/tungsten.spr',
		'isometal':		'bases/repair_upgrade/items/damaged/isometal.spr',
		# add-ons
		'afterburner':			'bases/repair_upgrade/items/damaged/afterburner.spr',
		'shield_4_Level1':			'bases/repair_upgrade/items/damaged/shields.spr',
		'shield_4_Level2':			'bases/repair_upgrade/items/damaged/shields.spr',
		'shield_4_Level3':			'bases/repair_upgrade/items/damaged/shields.spr',
		'shield_4_Level4':			'bases/repair_upgrade/items/damaged/shields.spr',
		'shield_4_Level5':			'bases/repair_upgrade/items/damaged/shields.spr',
		'shield_4_Level6':			'bases/repair_upgrade/items/damaged/shields.spr',
		'shield_4_Level7':			'bases/repair_upgrade/items/damaged/shields.spr',
	}
	try:
		sprite = sprites[item_name]
	except:
		# a blank sprite
		sprite = lookup_upgrade_sprite(item_name)
	return sprite

#
# lookup_disallowed_upgrades
#	This function determines which upgrades each ship type can install
#
def lookup_disallowed_upgrades():
	cp        = VS.getCurrentPlayer()
	player    = VS.getPlayerX(cp)
	ship_name = player.getFullname()
	if (quest.checkSaveValue(cp,"removed_BoostedSteltek",1)):
		rf = True
	else:
		rf = False

	if rf:
		disallowed = {
			'basic_armor':	1,
			'add_ablative_hull_coating':	1,
			'add_sublimative_hull_coating':	1,
		}

	else:
		disallowed = {
			'fusion_gun': 	1,
			'isometal': 	1,
			'gun_cooler': 	1,
			'mult_speed_enhancer':		1,
			'mult_thrust_enhancer':		1,
			'mult_shield_regenerator':	1,
			'repair_droid_advanced':	1,
			'basic_armor':	1,
			'add_ablative_hull_coating':	1,
			'add_sublimative_hull_coating':	1,
		}

	if ship_name == 'tarsus':
		disallowed['add_cargo_expansion']   = 1
		disallowed['add_cargo_volume_galaxy']   = 1

		# no turrets
		disallowed['medium_turret_meson']        = 1
		disallowed['medium_turret_rear_meson']   = 1
		disallowed['medium_turret_bottom_meson'] = 1
		# shields
		disallowed['shield_4_Level4']        = 1
		disallowed['shield_4_Level5']        = 1
		disallowed['shield_4_Level6']        = 1
		disallowed['shield_4_Level7']        = 1
		# engines
		disallowed['reactor_level_4']        = 1
		disallowed['reactor_level_5']        = 1
		disallowed['reactor_level_6']        = 1
		disallowed['reactor_level_7']        = 1

		if (not rf):
			disallowed['shield_4_Level3']        = 1
			disallowed['reactor_level_3']        = 1
			disallowed['reactor_level_2']        = 1

	elif ship_name == 'centurion':
		# rear turret only
		disallowed['medium_turret_meson']        = 1
		disallowed['medium_turret_bottom_meson'] = 1
		disallowed['add_cargo_expansion']   = 1
		disallowed['add_cargo_volume']   = 1
		disallowed['add_cargo_volume_galaxy']   = 1
		# shields
		disallowed['shield_4_Level5']        = 1
		disallowed['shield_4_Level6']        = 1
		disallowed['shield_4_Level7']        = 1
		# engines
		disallowed['reactor_level_5']        = 1
		disallowed['reactor_level_6']        = 1
		disallowed['reactor_level_7']        = 1

		if (not rf):
			disallowed['shield_4_Level4']        = 1
			disallowed['reactor_level_4']        = 1

	elif ship_name == 'orion':
		# rear turret only
		disallowed['medium_turret_meson']        = 1
		disallowed['medium_turret_bottom_meson'] = 1
		disallowed['add_cargo_volume_galaxy']   = 1
		disallowed['add_cargo_volume']   = 1

		if (not rf):
			disallowed['shield_4_Level6']        = 1
			disallowed['shield_4_Level7']        = 1
			disallowed['reactor_level_6']        = 1
			disallowed['reactor_level_7']        = 1

	elif ship_name == 'galaxy':
		# top/bottom turrets only
		disallowed['medium_turret_rear_meson']   = 1
		disallowed['add_cargo_volume']   = 1
		disallowed['add_cargo_expansion']   = 1

		# shields
		disallowed['shield_4_Level5']        = 1
		disallowed['shield_4_Level6']        = 1
		disallowed['shield_4_Level7']        = 1
		# engines
		disallowed['reactor_level_5']        = 1
		disallowed['reactor_level_6']        = 1
		disallowed['reactor_level_7']        = 1

		if (not rf):
			disallowed['shield_4_Level4']        = 1
			disallowed['reactor_level_4']        = 1

	else:
		# this is a catch-all for other ships, in case of expansion (using demon, drayman, talon, etc)
		# no turrets
		disallowed['medium_turret_meson']        = 1
		disallowed['medium_turret_rear_meson']   = 1
		disallowed['medium_turret_bottom_meson'] = 1
		# no cargo
		disallowed['add_cargo_volume']   = 1
		disallowed['add_cargo_expansion']   = 1
		disallowed['add_cargo_volume_galaxy']   = 1
		# no jump drive
		disallowed['jump_drive']   = 1
		# shields
		disallowed['shield_4_Level4']        = 1
		disallowed['shield_4_Level5']        = 1
		disallowed['shield_4_Level6']        = 1
		disallowed['shield_4_Level7']        = 1
		# engines
		disallowed['reactor_level_4']        = 1
		disallowed['reactor_level_5']        = 1
		disallowed['reactor_level_6']        = 1
		disallowed['reactor_level_7']        = 1

	return disallowed


#
# sort the buy/sell/repair lists like the original Privateer
#
def lookup_upgrade_sort_order(item_name):
	sort_order = {
		# shields
		'shield_4_Level1':		17,
		'shield_4_Level2':		17,
		'shield_4_Level3':		17,
		'shield_4_Level4':		17,
		'shield_4_Level5':		17,
		'shield_4_Level6':		17,
		'shield_4_Level7':		17,
		# engines
		'reactor_level_1':		18,
		'reactor_level_2':		18,
		'reactor_level_3':		18,
		'reactor_level_4':		18,
		'reactor_level_5':		18,
		'reactor_level_6':		18,
		'reactor_level_7':		18,
		# guns
		'laser':			1,
		'mass_driver':		2,
		'meson_blaster':	3,
		'neutron_gun':		4,
		'particle_cannon':	5,
		'tachyon_cannon':	6,
		'ion':				7,
		'plasma_gun':		8,
		'fusion_gun':		9,
		'steltek_gun':				9,
		'steltek_gun_boosted':		9,
		# missles
		'missile_launcher':			10,
		'dumbfire_ammo':			13,
		'heatseeker_ammo':			14,
		'image_recognition_ammo':	15,
		'friend_or_foe_ammo':		16,
		# torpedos
		'torpedo_launcher':			11,
		'proton_torpedo_ammo':		12,
		# armor
		'plasteel':		20,
		'tungsten':		21,
		'isometal':		22,
		# add-ons
		'afterburner':			19,
		'tractor_beam':					23,
		'jump_drive':			24,
		'repair_droid':			25,
		'repair_droid_advanced':		26,
		'ecm_package_1':		27,
		'ecm_package_2':		28,
		'ecm_package_3':		29,
		'add_cargo_volume':		30,
		'add_cargo_expansion':		31,
		'add_cargo_volume_galaxy':		32,
		'medium_turret_meson':			33,
		'medium_turret_rear_meson':		34,
		'medium_turret_bottom_meson':	35,
		# rf add-ons
		'gun_cooler':				36,
		'mult_speed_enhancer':		37,
		'mult_thrust_enhancer':		38,
		'mult_shield_regenerator':	39,
		}
	try:
		n = sort_order[item_name]
	except:
		# not in list
		n = 40
	return n

def sort_upgrades(a,b):
	x = lookup_upgrade_sort_order(a)
	y = lookup_upgrade_sort_order(b)
	if x < y:
		return -1
	elif x > y:
		return 1
	else:
		# fall back on item name
		if a < b:
			return -1
		elif a > b:
			return 1
		return 0

def sort_upgrades_sell(a,b):
	return sort_upgrades(a[0],b[0])

def sort_missiles(a,b):
	player = VS.getPlayer()
	x = player.GetMountInfo(a)
	y = player.GetMountInfo(b)
	if x['ammo'] > y['ammo']:
		return -1
	elif x['ammo'] < y['ammo']:
		return 1
	else:
		return 0

# 
# create lists showing what can be bought, sold, or repaired
#
def get_upgrade_repair_list(upgrades): #, basic_repair_cost):
	repair = []
	for i in range(len(upgrades)):
		# temporarily make the item damaged
#		upgrades[i][1] = 0.75
		if (upgrades[i][1] < 1.0):
			# only store the index to item in the sell list
			repair.append( i )

#	if basic_repair_cost > 0:
#		repair.append( -1 )

	# temporary
#	print "::: get_upgrade_repair_list"
	print ("::: get_upgrade_repair_list")
	import pprint
	pprint.pprint( repair )

	return repair

def get_upgrade_sell_list():
	sell = []
	player = VS.getPlayer()

	# add cargo-type ship upgrades
	for i in range(player.numCargo()):
		cargo = player.GetCargoIndex(i)
		category = cargo.GetCategory()
		if category[:8]  != 'upgrades': continue
		if category[:14] == 'upgrades/Radar': continue
		if category[:22] == 'upgrades/Damaged/Radar': continue
		name = cargo.GetContent()
		try:
#			damage = cargo.GetFunctionality()/cargo.GetMaxFunctionality()
			damage = player.PercentOperational(name, category, False)
		except:
			damage = 1.0

		if damage > 0.0:
			# item_name, damage, type, mount, quantity
			sell.append( [name, damage, 'cargo', None, None] )
		else:
			# remove it from the ship completely if it's down to 0% functional
			remove_item(player, name, cargo.GetQuantity(), False)	 # note: False means don't call RecomputeUnitUpgrades()

	# add guns, missiles, and launchers
	for i in range(player.getNumMounts()):
		mount = player.GetMountInfo(i)

		try:
#			damage = mount['functionality']/mount['maxfunctionality']
			(func, maxfunc, status) = player.MountPercentOperational(i)
			damage = func/maxfunc
		except:
			damage = 1.0

		# if this mount is occupied, allow sale
		if (not mount['empty']):
			try:
				name = mount['weapon_info']['name']
			except:
				name = ''
			display_name = lookup_item_name(name)
			quantity = int(mount['ammo'])
			if damage > 0.0:
				if (quantity > 0):
					# since percent operational for missiles also applies to launchers, 
					# apply damage here, but not where we append *_launcher below
					sell.append( [display_name, damage, 'missile', i, quantity] )
				elif (quantity == -1):
					# weapons have ammo set to -1
					sell.append( [display_name, damage, 'weapon', i, None] )
			else:
				remove_upgrade(player, display_name, i)

		# check whether this is a missile launcher
		if (mount['size'] & 64) or (mount['size'] & 128):
			# light-missile or medium-missile launcher
			sell.append( ['missile_launcher', 1.0, 'launcher', i, None] )
		elif (mount['size'] & 256):
			# heavy-missile (torpedo) launcher
			sell.append( ['torpedo_launcher', 1.0, 'launcher', i, None] )

	# add turrets
	sub_units = player.getSubUnits()		# returns a un_iter class
	i = 0
	while not (sub_units.isDone()):
		current_sub_unit = sub_units.current()
		item_name   = lookup_item_name( current_sub_unit.getFullname() )
		damage = current_sub_unit.GetHullPercent() # is this the right way to show damage?
		# this only works for galaxy; if other ships are added (paradigm, drayman, etc) this will likely break
		if i > 0 and item_name == "medium_turret_meson":
			item_name = "medium_turret_bottom_meson"
		# don't include blank turrets
		blank_turrets = [ 
			"medium_blank", "mediumrear_blank", 				# old units.csv entries (for old savegames)
			"turret_medium_blank", "turret_mediumrear_blank"	# new units.csv entries
			]
		if item_name in blank_turrets:  pass
		else:
			if damage > 0.0:
				sell.append( [item_name, 1.0, 'subunit', None, None] )
			else:
				remove_turret(player, item_name)
		i = i + 1
#		sub_units.next()
		next(sub_units)
#	sell.sort(sort_upgrades_sell)

	# temporary
#	print "::: get_upgrade_sell_list"
	print ("::: get_upgrade_sell_list")
	import pprint
	pprint.pprint( sell )

	return sell

def get_upgrade_buy_list(prices, disallowed):
	buy = []
#	keys = prices.keys()
	keys = list(prices.keys())
	# sort the list of upgrades
#	keys.sort(sort_upgrades)
	for i in keys:
		# if it's not in prohibited upgrade list for this ship, add to buy list
		try:
			if (disallowed[i]):
				pass
		except:
			buy.append( i )
	return buy

#
# RepairBayComputerAnimation
#	pop-up computer animation
#	this also resets the RepairBayComputer when coming from the ship dealer
#
class RepairBayComputerAnimation:
	def __init__(self,room_start, room_next, upgradename, use_ship_320_240_upgrade):
		# create GUIRoom object
		guiroom  = GUI.GUIRoom(room_start)
		self.guiroom = guiroom
		self.room_next  = room_next

		# let us find this object via GUIRootSingleton.rooms[x].owner or GUIElement.room.owner
		guiroom.owner = self

		# draw the background image

		# PlayerShip module uses Base.Texture/Base.Ship directly, instead of GUI.GUIStaticImage
		# so, background sprite has to be drawn using Base.Texture as well, or the order is messed up
		x=0
		y=0
		if use_ship_320_240_upgrade:
			x=0.582
			y=-0.2716
		Base.Texture (room_start, 'background', upgradename+'.spr', x, y)

		# sometimes python errors cause the Base.RunScript call to fail; in that case, add a way out of the animation
		Base.Link (room_start, 'out_of_animation', 0.75, 0.75, 0.25, 0.25, 'Next', room_next)
 
	 	# add ship sprite
		PlayerShip.AddPlayerShips('shipupgrade',room_start,'repairship')
		# add computer animation
		self.computer   = GUI.GUIStaticImage(guiroom, 'animation', ( 'bases/repair_upgrade/ani.spr', GUI.GUIRect(0, 99, 160, 100) )) #GUI.GUIRect(0, 0, 320, 200) ))

		# draw now
		GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index, 'draw', None)

		# undraw the animation, so that when reset is called, it runs from the beginning
		# NOTE: using hide() here doesn't work, as of the current version of GUI.py
		# calling guiroom.redrawIfNeeded somewhere in the reset() or Base.RunScript() code would probably fix this
		self.computer.undraw()

	def reset(self):
		room_start = self.guiroom.getIndex()
		room_next  = self.room_next

		self.computer.draw()

		# reset the repair bay computer to buy mode
		GUI.GUIRootSingleton.rooms[room_next].owner.reset()

		# add script which will automatically switch from intro to main page
		Base.RunScript(room_start, "redirect", """#
import Base
Base.SetCurRoom(%s)
Base.EraseObj(%s,"redirect")
import GUI
GUI.GUIRootSingleton.rooms[%s].owner.computer.undraw()
""" %(room_next, room_start, room_start), 2.0)

class RepairBayComputerGeneric:
	def __init__(self):
		self.buy    = []
		self.sell   = []
		self.repair = []
		self.disallowed = {}

		# set up buy, sell and repair prices
		self.buy_prices    = {}
		self.sell_prices   = {}
		self.repair_prices = {}
		# get list of ship upgrade units
		global master_part_list
		upgrade_list = master_part_list.getUpgradeList()
		for cargo in upgrade_list:
			name = cargo.GetContent()
			try:
				buy_price    = int( cargo.GetPrice() )
				sell_price   = int( buy_price * 0.5 )
				repair_price = int( buy_price * 0.35 )
				self.buy_prices[name]    = buy_price
				self.sell_prices[name]   = sell_price
				self.repair_prices[name] = repair_price
			except:
				pass
		
#		if VS.isserver():
#			self.basic_repair_cost = VS.getPlayer().RepairCost()
#		else:
#			global basic_repair_cost
#			self.basic_repair_cost = basic_repair_cost
		self.reset()
	def draw(self, text):
		self.status = text
	def reset(self):
		# also, rebuild the buy/sell/repair lists, in case user sold ship
		self.disallowed = lookup_disallowed_upgrades()
		self.buy    = get_upgrade_buy_list(self.buy_prices, self.disallowed)
		self.sell   = get_upgrade_sell_list()
		self.repair = get_upgrade_repair_list(self.sell) #, self.basic_repair_cost)
		
		self.upgrade_classes = {}
		for i in range(len(self.sell)):
			item_name, undamaged, type, mount_num, quantity = self.sell[i]
			if type == "weapon":
				pass
			elif type == "missile":
				pass
			else:
				upgrade_class = lookup_upgrade_class(item_name)
				self.upgrade_classes[upgrade_class] = item_name

		#   enum MOUNT_SIZE {NOWEAP=0x0,LIGHT=0x1,MEDIUM=0x2,HEAVY=0x4,CAPSHIPLIGHT=0x8,CAPSHIPHEAVY=0x10,SPECIAL=0x20, LIGHTMISSILE=0x40,MEDIUMMISSILE=0x80,HEAVYMISSILE=0x100,CAPSHIPLIGHTMISSILE=0x200, CAPSHIPHEAVYMISSILE=0x400,SPECIALMISSILE=0x800, AUTOTRACKING=0x1000} size;
		self.mounts = {
			'missile': [],
			'torpedo': [],
			'gun':     [],
			'special': [],
			'empty':   {}
			}
		player = VS.getPlayer()
		for i in range(player.getNumMounts()):
			mount = player.GetMountInfo(i)
			# check whether mount is used or not
			self.mounts['empty'][i] = mount['empty']
			
			# check what type of mount this is
			if (mount['size'] & 1) or (mount['size'] & 2) or (mount['size'] & 4):
				self.mounts['gun'].append(i)
			if (mount['size'] & 32):
				self.mounts['special'].append(i)
			if (mount['size'] & 64) or (mount['size'] & 128):
				self.mounts['missile'].append(i)
				# missile mounts aren't empty

				self.mounts['empty'][i] = False
			if (mount['size'] & 256):
				self.mounts['torpedo'].append(i)
				# torpedo mounts aren't empty
				self.mounts['empty'][i] = False
			if mount['empty']==False:
#				print mount['weapon_info']
				print (mount['weapon_info'])
		
	def setstatus(self,success,message):
		self.status = [success and "success" or "failure", message]
	#def draw(self,message=None):
	#	pass
	#def drawBlank(self,message=None):
	#	pass
	def resetstatus(self):
		self.status = ["failure", "Unknown error"]

	def handle_server_cmd(self, args):
		cmd = args[0]
		if cmd == "buy":
			return self.buy_server(args[1])
		elif cmd == "sell":
			return self.sell_server(args[1], args[2])
		elif cmd == "repair":
			self.repair = get_upgrade_repair_list(self.sell) #, self.basic_repair_cost)
			return self.repair_server(args[1])
		elif cmd == "mount_select_buy":
			return self.mount_select_buy_server(args[1], args[2])
		elif cmd == "reload":
			self.reset()
			return ["success", "Reloaded"]
		else:
			return ["failure", "Error: subcommand %s not valid" % args[0]]

	def weapon_bought(self, item_name, type, mount_num):
		self.sell.append( [item_name, 1.0, type, mount_num, None])
		self.mounts['empty'][mount_num] = False
	def launcher_bought(self, item_name, type, mount_num):
		self.sell.append( [item_name, 1.0, type, mount_num, None])
		self.mounts['empty'][mount_num] = False
		if item_name == "missile_launcher":
			self.mounts['missile'].append(mount_num)
		elif item_name == "torpedo_launcher":
			self.mounts['torpedo'].append(mount_num)
	def missile_bought(self, item_name, type, mount_num):
		self.sell = get_upgrade_sell_list()
	def cargo_bought(self, item_name, type, upgrade_class):
		self.sell.append( [item_name, 1.0, type, None, None])
		self.upgrade_classes[upgrade_class] = item_name

	def mount_select_buy_server(self, item_name, mount_num):
		self.resetstatus()
		if item_name not in self.buy:
#			print "ERROR: "+item_name+" mount not in self.buy which is: "+repr(self.buy)
			print ("ERROR: "+item_name+" mount not in self.buy which is: "+repr(self.buy))
			#return
		try:
			mount_num = int(mount_num)
		except:
			pass
		type      = lookup_upgrade_type(item_name)
		try:
			price = int( self.buy_prices[item_name] )
		except:
			price = 0
		player = VS.getPlayer()
		if (player.getCredits() < price):
			self.setstatus(False, "INSUFFICIENT CREDIT")
		elif type == "weapon":
			success = add_upgrade(player, item_name, mount_num, 0, 0, 0)
			if success:
				player.addCredits(-1 * price)
				self.weapon_bought(item_name,type,mount_num)
				self.setstatus(True, "Thank You")
			else:
				self.setstatus(False, "ERROR: Can't add %s to %s" %(item_name, mount_num) )
		elif type == "launcher" or type == "tractor":
			success = add_upgrade(player, item_name, mount_num, 0, 0, 0)
			if success:
				player.addCredits(-1 * price)
				self.launcher_bought(item_name,type,mount_num)
				self.setstatus(True, "Thank You")
			else:
				self.setstatus(False, "ERROR: Can't add %s to %s" %(item_name, mount_num) )
		elif type == "missile" or type == "torpedo":
			#self.mounts['empty'][mount_num] = False
			# add_upgrade returns false for missiles, so we just have to ignore the result
			success = add_upgrade(player, item_name, mount_num, 0, 0, 0)
			player.addCredits(-1 * price)
			# just reload the whole list, rather than try to add a single missile to the lista
			self.missile_bought(item_name,type,mount_num)
			self.setstatus(True, "Thank You")
		return self.status
	
	def buy_server(self, item_name):
		self.resetstatus()
		if item_name not in self.buy:
#			print "ERROR: "+item_name+" mount not in self.buy which is: "+repr(self.buy)
			print ("ERROR: "+item_name+" mount not in self.buy which is: "+repr(self.buy))
			#return
		type      = lookup_upgrade_type(item_name)
		try:
			price = int( self.buy_prices[item_name] )
		except:
			price = 0
		player = VS.getPlayer()
		if (player.getCredits() < price):
			self.setstatus(False, "INSUFFICIENT CREDIT")
		elif type == "cargo":
			upgrade_class = lookup_upgrade_class(item_name)
			has_item = self.upgrade_classes.get(upgrade_class, '')
			if has_item == '':
				# deduct cost
				player.addCredits(-1 * price)
				# add item to ship
				if add_item(player, item_name, price, 1):
				# add item to buy/sell computer datastructures
					self.cargo_bought( item_name, type, upgrade_class)
					# draw the screen
					self.setstatus(True, "Thank You")
				else:
					self.setstatus(False, "ERROR: Can't add %s" %(item_name) )
			else:
				self.setstatus(False, "NO ROOM ON SHIP")
		elif type == "subunit":
			upgrade_class = lookup_upgrade_class(item_name)
			try:
				has_item = self.upgrade_classes[upgrade_class]
			except:
				has_item = ''
			if has_item == '':
				success = add_turret(player, item_name)
				if success:
					player.addCredits(-1 * price)
					self.cargo_bought(item_name, type, upgrade_class)
					self.setstatus(True, "Thank You")
				else:
					self.setstatus(False, "ERROR: Can't add %s to %s" %(item_name, mount_num) )
			else:
				self.setstatus(False, "NO ROOM ON SHIP")
		else:
			# error - unknown type
			self.setstatus(False, "ERROR: Unknown server upgrade type %s" %(type.upper()) )
		return self.status

	def cargo_sold(self, item_name, current_item):
		self.sell.pop(current_item)
		upgrade_class = lookup_upgrade_class(item_name)
		self.upgrade_classes[upgrade_class] = ''
	def weapon_sold(self, item_name, current_item, mount_num):
		self.sell.pop(current_item)
		if mount_num in self.mounts['missile'] or mount_num in self.mounts['torpedo']:
			self.mounts['empty'][mount_num] = False
		else:
			self.mounts['empty'][mount_num] = True

	def sell_server(self, item_name_sent, mount_num_sent):
		self.resetstatus()
		if (len(self.repair) > 0) and (len(self.sell) > 0):
			# this first if statement is needed due to the way the sell code works
			# if we ever get a VS.downgrade to remove a single item, then this
			# can be removed
			self.setstatus(False, "YOU MUST REPAIR DAMAGED ITEMS" )
			return self.status
		# if there is stuff to sell
		item_name = ''
		current_item = 0
		mount_num = 0
		for sellitem in self.sell:
			if sellitem[0]==item_name_sent and str(sellitem[3])==mount_num_sent:
				item_name, undamaged, type, mount_num, quantity = sellitem
				break
			current_item += 1
		if item_name:
			try:
				price = int( self.sell_prices[item_name] * undamaged )
			except:
				price = 0
			player = VS.getPlayer()
			if type == "cargo":
				# selling a cargo-type upgrade (afterburner, repair droid, ecm, jump drive, etc)
				if remove_item(player, item_name, 1):
					player.addCredits(price)
					self.cargo_sold(item_name, current_item)
					# remove item from upgrade_class list
					self.setstatus(True, "Thank You")
				else:
					self.setstatus(False, "ERROR: Cannot remove %s" %(item_name.upper()))
			elif type == "weapon" or type == "tractor":
				# selling a gun or tractor beam
				try:
					if remove_upgrade(player,item_name,mount_num):
						player.addCredits(price)
						self.weapon_sold(item_name, current_item, mount_num)
						self.setstatus(True, "Thank You")
					else:
						self.setstatus(False, "ERROR: Cannot remove %s" %(item_name.upper()))
				except:
					self.setstatus(False, "ERROR: Cannot remove %s" %(item_name.upper()))
			elif type == "missile" or type == "torpedo":
				# selling a missile/torpedo
				try:
					# there is no way to give a quantity to removeWeapon, so just
					# treat it like select_all is always true
					select_all = True
					if remove_upgrade(player, item_name, mount_num):
						#self.mounts['empty'][mount_num] = True
						if select_all:
							price = price * quantity
							quantity = 0
						else:
							quantity = quantity - 1
						player.addCredits(price)
						# remove one from current quantity
						if quantity > 0:
							self.sell[current_item][4] = quantity
						else:
							self.sell.pop(current_item)
						self.setstatus(True, "Thank You")
					else:
						self.setstatus(False, "ERROR: Cannot remove %s" %(item_name.upper()))
				except:
					self.setstatus(False, "ERROR: Cannot remove %s" %(item_name.upper()))
			elif type == "subunit":
				# selling a turret
				if remove_turret(player, item_name):
					player.addCredits(price)
					self.sell.pop(current_item)
					self.setstatus(True, "Thank You")
				else:
					self.setstatus(False, "ERROR: Cannot remove TURRET")
			else:
				self.setstatus(False, "ERROR: Unknown upgrade type %s" %(type.upper()) )
		else:
			self.setstatus(False, "ERROR: Can't find upgrade "+item_name_sent)
		return self.status
	
	def repair_server(self, repair_index):
		self.resetstatus()
		try:
			repair_index = int(repair_index)
		except:
			pass
		player = VS.getPlayer()
		#self.repair = get_upgrade_repair_list(self.sell)
		if repair_index < 0 and repair_index not in self.repair:
			self.repair.append(-1)
		if repair_index in self.repair:
		#if len(self.repair) > 0:
		#	repair_index = self.repair[self.current_item]
			if repair_index >= 0:
				item_name, undamaged, type, mount_num, quantity = self.sell[repair_index]
				# repair cost is the fraction of functionality * the repair_price
				price = int( self.repair_prices[item_name] * (1.0 - undamaged) )
#			else:
				# "Basic Repair"
#				item_name = "basic_inspection"
#				global basic_repair_price
#				price = basic_repair_price * self.basic_repair_cost

			if player.getCredits() < price:
				self.setstatus(False, "INSUFFICIENT CREDIT")
			else:
#				if repair_index < 0:
					# do a "basic repair"
#					rc = player.RepairUpgrade()
#					self.repair.remove(repair_index) # Not pop -- this removes element whose value is arg
#					if (rc):
						# deduct cost, repair item, and set basic_repair_cost to 0
#						player.addCredits(-1 * price)
#						self.setstatus(True, "Thank You")
#					else:
#						self.setstatus(True, "NO DAMAGE FOUND: NO CHARGE")
					# don't show "basic repair" again while player is on this base
#					self.basic_repair_cost = 0

#				elif type == "cargo":
				if type == "cargo":
					if repair_item(player,item_name):
						# deduct cost, repair item, and update repair list
						player.addCredits(-1 * price)
						self.repair.remove(repair_index)
						self.sell[repair_index][1] = 1.0
						self.setstatus(True, "ITEM REPAIRED")
					else:
						self.setstatus(False, "ERROR: Cannot repair %s" %(item_name.upper()))
				elif type == "weapon" or type == "tractor" or type == "launcher":
					if repair_upgrade(player,item_name,mount_num):
						# deduct cost, repair item, and update repair list
						player.addCredits(-1 * price)
						self.repair.remove(repair_index)
						self.sell[repair_index][1] = 1.0
						self.setstatus(True, "ITEM REPAIRED")
					else:
						self.setstatus(False, "ERROR: Cannot repair %s" %(item_name.upper()))
				elif type == "missile" or type == "torpedo":
					# deduct repair price
					player.addCredits(-1 * price)
					# remove damaged missiles
					remove_upgrade(player, item_name, mount_num)
					# add <quantity> number of missiles
					for count in range(quantity):
						add_upgrade(player, item_name, mount_num, 0, 0, 0)
					# update repair and sell lists
					self.repair.remove(repair_index)
					self.sell[repair_index][1] = 1.0
					# tell player item is repaired
					self.setstatus(True, "ITEM REPAIRED")
				elif type == "subunit":
					if repair_turret(player,item_name):
						# deduct cost, repair item, and update repair list
						player.addCredits(-1 * price)
						self.repair.remove(repair_index)
						self.sell[repair_index][1] = 1.0
						self.setstatus(True, "ITEM REPAIRED")
					else:
						self.setstatus(False, "ERROR: Cannot repair %s" %(item_name.upper()))
		else:
			self.setstatus(False, "ERROR: Invalid repair index %d in %s" % (repair_index, repr(self.repair)))
		return self.status



class RepairBayComputer(RepairBayComputerGeneric):
	singleton = None
	def __init__(self,room_id):
		self.room_id  = room_id

		RepairBayComputer.singleton = self

		# initial state is "buy"
		self.state = "buy"
		self.enabled = 1
		guiroom = GUI.GUIRoom(room_id)
		self.guiroom = guiroom

		# when a button is clicked, this will allow us to get the RepairBayComputer instance from the x_click functions
		guiroom.owner = self
		
		# background and ship image sprites are drawn elsewhere
		# computer sprite:
		GUI.GUIStaticImage(guiroom, 'computer', ( 'bases/repair_upgrade/shipupgrade_computer.spr', GUI.GUIRect(0, 99, 160, 100) )) # , GUI.GUIRect(0, 0, 320, 200) )).draw()

		self.buttons = {}

		# main buttons
		repair_sprite = ('bases/repair_upgrade/buttons/button_repair.spr', GUI.GUIRect(51.5, 101, 36, 11))  # GUI.GUIRect(0, 0, 320, 200))
		buy_sprite    = ('bases/repair_upgrade/buttons/button_buy.spr',    GUI.GUIRect(81.5, 185, 28, 10))  # GUI.GUIRect(0, 0, 320, 200))
		sell_sprite   = ('bases/repair_upgrade/buttons/button_sell.spr',   GUI.GUIRect(35, 185, 28, 10))  # GUI.GUIRect(0, 0, 320, 200))
		repair_sprset = { 'checked': repair_sprite, 'unchecked': None, 'hot': repair_sprite }
		buy_sprset    = { 'checked': buy_sprite,    'unchecked': None, 'hot': buy_sprite }
		sell_sprset   = { 'checked': sell_sprite,   'unchecked': None, 'hot': sell_sprite }
		self.add_button( GUI.GUIButton(guiroom,      'Select Items',  'btn_select', {},            GUI.GUIRect(20, 114, 103, 67)), select_click )
		self.add_button( GUI.GUIRadioButton(guiroom, 'Repair Mode',   'btn_repair', repair_sprset, GUI.GUIRect(52, 102, 36, 11), 'repair_bay_comp_controls'), mode_click )
		self.add_button( GUI.GUIRadioButton(guiroom, 'Buy Mode',      'btn_buy',    buy_sprset,    GUI.GUIRect(82, 186, 28, 10), 'repair_bay_comp_controls'), mode_click )
		self.add_button( GUI.GUIRadioButton(guiroom, 'Sell Mode',     'btn_sell',   sell_sprset,   GUI.GUIRect(35, 186, 28, 10), 'repair_bay_comp_controls'), mode_click )
		self.add_button( GUI.GUIButton(guiroom,      'Previous Item', 'btn_prev',   {},            GUI.GUIRect(133, 148, 10, 17)), prev_click )
		self.add_button( GUI.GUIButton(guiroom,      'Next Item',     'btn_next',   {},            GUI.GUIRect(133, 129, 10, 17)), next_click )

		# set the check button state
		if (self.state == "buy"):
			GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index,'check',{'index':'btn_buy'})
		elif (self.state == "sell"):
			GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index,'check',{'index':'btn_sell'})
		elif (self.state == "repair"):
			GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index,'check',{'index':'btn_repair'})
	
		# add the text labels
		txt_color = GUI.GUIColor(0.7,0.7,0.7)
		txt_warning_color = GUI.GUIColor(0.7,0,0)
		self.txt_name     = GUI.GUIStaticText(guiroom,'txt_name',     '', GUI.GUIRect(24, 113, 99, 10), txt_color)
		self.txt_cost     = GUI.GUIStaticText(guiroom,'txt_cost',     '', GUI.GUIRect(24, 167, 99, 10), txt_color)
		self.txt_credits  = GUI.GUIStaticText(guiroom,'txt_credits',  '', GUI.GUIRect(24, 171, 99, 10), txt_color)
		self.txt_quantity = GUI.GUIStaticText(guiroom,'txt_quantity', '', GUI.GUIRect(24, 119, 99, 10), txt_color)
		self.txt_message  = GUI.GUIStaticText(guiroom,'txt_message',  '', GUI.GUIRect(24, 122, 99, 10), txt_warning_color)

		# add the item image
		self.img_item_rect = GUI.GUIRect(20, 114, 103, 67)
		self.img_item      = GUI.GUIStaticImage(guiroom, 'img_item', None)

		# add the mount selectors
		self.mount_selectors = {}
		# label, name, guirect, sprite, sprite_hot, call_func, hidden=True
		self.add_mount_selector("Mount 1", "btn_mount_1", GUI.GUIRect(180, 75, 13.125, 11), 'bases/repair_upgrade/buttons/mount_1.spr', 'bases/repair_upgrade/buttons/mount_1_on.spr', 0 )
		self.add_mount_selector("Mount 2", "btn_mount_2", GUI.GUIRect(195, 75, 13.125, 11), 'bases/repair_upgrade/buttons/mount_2.spr', 'bases/repair_upgrade/buttons/mount_2_on.spr', 1 )
		self.add_mount_selector("Mount 3", "btn_mount_3", GUI.GUIRect(210, 75, 13.125, 11), 'bases/repair_upgrade/buttons/mount_3.spr', 'bases/repair_upgrade/buttons/mount_3_on.spr', 2 )
		self.add_mount_selector("Mount 4", "btn_mount_4", GUI.GUIRect(225, 75, 13.125, 11), 'bases/repair_upgrade/buttons/mount_4.spr', 'bases/repair_upgrade/buttons/mount_4_on.spr', 3 )
		self.add_mount_selector("Mount 5", "btn_mount_5", GUI.GUIRect(240, 75, 13.125, 11), 'bases/repair_upgrade/buttons/mount_5.spr', 'bases/repair_upgrade/buttons/mount_5_on.spr', 4 )
		self.add_mount_selector("Mount 6", "btn_mount_6", GUI.GUIRect(255, 75, 13.125, 11), 'bases/repair_upgrade/buttons/mount_6.spr', 'bases/repair_upgrade/buttons/mount_6_on.spr', 5 )
		self.add_mount_selector("Cancel",  "btn_mount_c", GUI.GUIRect(270, 76, 30.3125, 7.1875), 'bases/repair_upgrade/buttons/mount_c.spr', 'bases/repair_upgrade/buttons/mount_c_on.spr', -1 )


		# draw all widgets on the screen
		GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index, 'draw', None)
		RepairBayComputerGeneric.__init__(self)

	def add_button(self, guibutton, onclick_handler):
		# add the button to the "buttons" dictionary, draw it, and add onclick handler
		self.buttons[guibutton.index] = guibutton
		guibutton.onClick = methodtype.methodtype(onclick_handler, guibutton, type(guibutton))

	def add_mount_selector(self, label, name, guirect, sprite, sprite_hot, mount_num=None):
		self.mount_selectors[name] = {
			'label':		label,
			'name':			name,
			'guirect':  	guirect,
			'sprite':		sprite,
			'sprite_hot':	sprite_hot,
			'mount_num':	mount_num
		}
		sprite_t      = (sprite,     guirect)
		hot_sprite_t  = (sprite_hot, guirect)
		sprite_set    = { '*': sprite_t, 'hot': hot_sprite_t }
		self.add_button( GUI.GUIRadioButton(self.guiroom, label, name, sprite_set, guirect, "mount_selectors"), mount_select_click )

	def move_mount_selector(self, name, guirect):
		selector = self.mount_selectors[name]
		button   = self.buttons[name]

		selector["guirect"] = guirect
		sprite     = selector['sprite']
		sprite_hot = selector['sprite_hot']
		button.sprites = { '*': (sprite, guirect), 'hot': (sprite_hot, guirect) }
		button.hotspot = guirect
		button.setState(button.state)
		button.notifyNeedRedraw()

	def hide_mount_selectors(self):
		self.enabled = 1
		for key in self.mount_selectors:
			self.buttons[key].hide()

	def show_mount_selectors(self, mounts):
		self.enabled = 0
		for key in self.mount_selectors:
			selector = self.mount_selectors[key]
			if selector["mount_num"] in mounts or selector["mount_num"] == -1:
				self.buttons[key].show()

	def reset(self):
		# reset computer to initial state
		
		if VS.networked():
			custom.run("RepairBayComputer", ["reload"], None)
		
		self.state = "buy"
		self.current_item = 0
		GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'check',{'index':'btn_buy'})

		# move the mount selectors around, if desired
		move_mounts = True
		if (move_mounts):
			w = 13.125 			# width, height of mount select buttons
			h = 11
			wc = 30.3125		# width, height of mount select cancel button
			hc = 7.1875
			ship_name = VS.getPlayer().getFullname()
			if ship_name == "tarsus":
				self.move_mount_selector("btn_mount_1", GUI.GUIRect(177, 67, w,  h))
				self.move_mount_selector("btn_mount_2", GUI.GUIRect(199, 67, w,  h))
				self.move_mount_selector("btn_mount_3", GUI.GUIRect(170, 82, w,  h))
				self.move_mount_selector("btn_mount_4", GUI.GUIRect(227, 82, w,  h))
				self.move_mount_selector("btn_mount_c", GUI.GUIRect(90, 168, wc, hc))	# cancel button
			elif ship_name == "orion":
				self.move_mount_selector("btn_mount_1", GUI.GUIRect(183, 101, w,  h))
				self.move_mount_selector("btn_mount_2", GUI.GUIRect(277, 101, w,  h))
				self.move_mount_selector("btn_mount_c", GUI.GUIRect(90, 168, wc, hc))	# cancel button
			elif ship_name == "galaxy":
				self.move_mount_selector("btn_mount_1", GUI.GUIRect(172, 78, w,  h))
				self.move_mount_selector("btn_mount_2", GUI.GUIRect(195, 78, w,  h))
				self.move_mount_selector("btn_mount_3", GUI.GUIRect(196, 28, w,  h))
				self.move_mount_selector("btn_mount_4", GUI.GUIRect(217, 28, w,  h))
				self.move_mount_selector("btn_mount_c", GUI.GUIRect(90, 168, wc, hc))	# cancel button
			elif ship_name == "centurion":
				self.move_mount_selector("btn_mount_1", GUI.GUIRect(125, 83, w,  h))
				self.move_mount_selector("btn_mount_2", GUI.GUIRect(140, 83, w,  h))
				self.move_mount_selector("btn_mount_3", GUI.GUIRect(278, 80, w,  h))
				self.move_mount_selector("btn_mount_4", GUI.GUIRect(297, 80, w,  h))
				self.move_mount_selector("btn_mount_5", GUI.GUIRect(148, 90, w,  h))
				self.move_mount_selector("btn_mount_6", GUI.GUIRect(287, 87, w,  h))
				self.move_mount_selector("btn_mount_c", GUI.GUIRect(90, 168, wc, hc))	# cancel button
			else:
				# this spot should be used to return the buttons to their default
				# positions, if additional ships are ever added
				pass


		self.hide_mount_selectors()

		RepairBayComputerGeneric.reset(self)
#		print "MOUNT UP"
		print ("MOUNT UP")
#		print self.mounts
		print (self.mounts)

		# call computer.draw() to place the right text and graphics on the screen
		self.draw()
		self.guiroom.redrawIfNeeded()

	def next(self):
		# disable button if mount_selectors are shown
		if not self.enabled: return
		if self.state=="buy":
			max = len(self.buy)
			if max > 0:
				self.current_item = (self.current_item + 1) % max
			else:
				self.current_item = 0
			
		elif self.state=="sell":
			max = len(self.sell)
			if max > 0:
				self.current_item = (self.current_item + 1) % max
			else:
				self.current_item = 0
		elif self.state=="repair":
			max = len(self.repair)
			if max > 0:
				self.current_item = (self.current_item + 1) % max
			else:
				self.current_item = 0
		self.draw()

	def previous(self):
		# disable button if mount_selectors are shown
		if not self.enabled: return
		if self.state=="buy":
			max = len(self.buy) - 1
			self.current_item = self.current_item - 1
			if (self.current_item < 0):
				self.current_item = max

		elif self.state=="sell":
			max = len(self.sell) - 1
			self.current_item = self.current_item - 1
			if (self.current_item < 0):
				self.current_item = max
		elif self.state=="repair":
			max = len(self.repair) - 1
			self.current_item = self.current_item - 1
			if (self.current_item < 0):
				self.current_item = max
		self.draw()

	def mount_select(self, button_index): 
		self.hide_mount_selectors()
		selector = self.mount_selectors[button_index]
		mount_num = selector["mount_num"]
		if self.state == "buy" and len(self.buy) > 0:
			# get the current_item from the list of things to buy
			item_name = self.buy[self.current_item]
			type      = lookup_upgrade_type(item_name)
			self.buy_selected_mount(item_name, type, mount_num)
	def buy_selected_mount(self, item_name, type, mount_num):
		if mount_num < 0:
			# cancel
			self.draw()
		else:
			def handleBuyResponse(args):
				if args[0]!='success':
					self.draw(args[1])
					return
				if VS.networked():
					if type == "weapon":
						self.weapon_bought(item_name, type, mount_num)
					elif type == "launcher" or type == "tractor":
						self.launcher_bought(item_name, type, mount_num)
					elif type == "missile" or type == "torpedo":
						self.missile_bought(item_name, type, mount_num)
				self.draw(args[1])
			# custom.run should be the last thing that happens...
			# it might either be synchronous or asynchronous (sort-of a bug)
			custom.run("RepairBayComputer", ["mount_select_buy",item_name,mount_num], handleBuyResponse)

	def select(self,select_all=False): 
		# disable button if mount_selectors are shown
		if not self.enabled: return
		if self.state == "repair":
			if len(self.repair) > 0:
				player = VS.getPlayer()
				repair_index = self.repair[self.current_item]
				if repair_index >= 0:
					item_name, undamaged, type, mount_num, quantity = self.sell[repair_index]
					# repair cost is the fraction of functionality * the repair_price
					price = int( self.repair_prices[item_name] * (1.0 - undamaged) )
#				else:
					# "Basic Repair"
#					item_name = "basic_inspection"
#					global basic_repair_price
#					global basic_repair_cost
#					price = basic_repair_price * basic_repair_cost
				
				def handleRepairResponse(args):
					if args[0]!='success':
						self.draw(args[1])
						return
#					if repair_index < 0:
						# Quirking around the fact that server-side can't use globals.
#						global basic_repair_cost
#						basic_repair_cost = 0
					if VS.networked():
						# The class isn't shared in this case...
						if repair_index < 0:
							self.repair.pop(self.current_item)
						elif type == "cargo":
							self.repair.pop(self.current_item)
							self.sell[repair_index][1] = 1.0
						elif type == "weapon":
							self.weapon_sold(item_name, self.current_item, mount_num)
						elif type == "subunit" or type == "missile" or type == "torpedo":
							self.repair.pop(self.current_item)
					if self.current_item > 0:
						self.current_item = self.current_item - 1
					self.drawBlank(args[1])

				if player.getCredits() < price:
					self.draw("INSUFFICIENT CREDIT")
				else:
					custom.run("RepairBayComputer", ["repair",repair_index], handleRepairResponse)
		
		elif self.state == "sell":
			if (len(self.repair) > 0) and (len(self.sell) > 0):
				# this first if statement is needed due to the way the sell code works
				# if we ever get a VS.downgrade to remove a single item, then this
				# can be removed
				self.draw( "YOU MUST REPAIR DAMAGED ITEMS" )
			elif len(self.sell) > 0:
				# if there is stuff to sell
				item_name, undamaged, type, mount_num, quantity = self.sell[self.current_item]
				def handleSellResponse(args):
					if args[0]!='success':
						self.draw(args[1])
						return
					if VS.networked():
						# The class isn't shared in this case...
						if type == "cargo":
							self.cargo_sold(item_name, self.current_item)
						elif type == "weapon":
							self.weapon_sold(item_name, self.current_item, mount_num)
						elif type == "subunit" or type == "missile" or type == "torpedo":
							self.sell.pop(self.current_item)
					if self.current_item > 0:
						self.current_item = self.current_item - 1
					self.draw(args[1])
				if type == "launcher":
					# selling a missile/torpedo launcher

					#
					# NOTE: this is due to lack of functionality in the Vegastrike Python API.
					#  Hopefully that will be fixed when the VS upgrade code gets rewritten
					#
					self.draw("CANNOT SELL LAUNCHERS")
				else:
					custom.run("RepairBayComputer", ["sell",item_name,mount_num], handleSellResponse)

		elif self.state == "buy":
			if len(self.buy) > 0:
				# get the current_item from the list of things to buy
				item_name = self.buy[self.current_item]
				type      = lookup_upgrade_type(item_name)
				player = VS.getPlayer()
				try:
					price = int( self.buy_prices[item_name] )
				except:
					price = 0
				def handleBuyResponse(args):
					if args[0]!='success':
						self.draw(args[1])
						return
					if VS.networked():
						if type == "cargo" or type == "subunit":
							upgrade_class = lookup_upgrade_class(item_name)
							self.cargo_bought(item_name, type, upgrade_class)
					self.draw(args[1])
				if (player.getCredits() < price):
					self.draw("INSUFFICIENT CREDIT")
				elif type == "cargo" or type == "subunit":
					#upgrade_class = lookup_upgrade_class(item_name)
					#has_item = self.upgrade_classes.get(upgrade_class, '')
					custom.run("RepairBayComputer", ["buy",item_name], handleBuyResponse)
				elif type == "weapon":
					# buying a gun 
					slots = available_mounts(self.mounts, 'gun')
					if len(slots) == 0:
						self.draw("NO ROOM ON SHIP")
					elif len(slots) == 1:
						mount_num = slots[0]
						self.buy_selected_mount(item_name, type, mount_num)
					else:
						self.show_mount_selectors(slots)
						self.draw("CHOOSE MOUNT")
				elif type == "launcher" or type == "tractor":
					# buying a missile/torpedo launcher
						slots = available_mounts(self.mounts, 'special',type=="tractor")
						if len(slots) == 0:
							self.draw("NO ROOM ON SHIP")
						elif len(slots) == 1:
							mount_num = slots[0]
							self.buy_selected_mount(item_name, type, mount_num)
						else:
							self.show_mount_selectors(slots)
							self.draw("CHOOSE MOUNT")
				elif type == "missile" or type == "torpedo":
					# buying a missile/torpedo
					if (player.getCredits() < price):
						self.draw("INSUFFICIENT CREDIT")
					else:
						slots = available_missile_mounts(self.mounts, type, item_name)
						if len(slots) == 0:
							self.draw("NO ROOM ON SHIP")
# disable mount selection for missiles - too cumbersome
#						elif len(slots) == 1:
						else:
							slots.sort(sort_missiles)
							mount_num = slots[0]
							self.buy_selected_mount(item_name, type, mount_num)
#						else:
#							self.show_mount_selectors(slots)
#							self.draw("CHOOSE MOUNT")
				else:
					# error - unknown type
					self.draw( "ERROR: Unknown upgrade type %s" %(type.upper()) )

	def set_state(self, button_index):
		# disable button if mount_selectors are shown
		if not self.enabled: return
		if button_index == "btn_buy":
			if self.state != "buy":
				self.state = "buy"
				self.current_item = 0
				self.draw()
		elif button_index == "btn_sell":
			if self.state != "sell":
				
				# sort the list first, if we added any new entries
#				self.sell.sort(sort_upgrades_sell)
				self.state = "sell"
				self.current_item = 0
				self.draw()
		elif button_index == "btn_repair":
			if self.state != "repair":
				# if a "basic repair" is needed, just do it
#				global basic_repair_cost
				player = VS.getPlayer()
				rc = player.RepairUpgrade()
#				print "::: calling player.RepairUpgrade()"
#				print rc
				print ("::: calling player.RepairUpgrade()")
				print (rc)
				# update the repair list, if user sold any damaged items since reset()
				self.repair = get_upgrade_repair_list(self.sell) #, basic_repair_cost)
				self.state = "repair"
				self.current_item = 0
				self.draw()
		# else: state is unknown

	def draw(self,message=None):
		if self.state == "buy":
			if len(self.buy):
				item_name = self.buy[self.current_item]
				display_name = lookup_upgrade_name(item_name)
				sprite       = lookup_upgrade_sprite(item_name)
				price = int( self.buy_prices[item_name] )
				self.drawItem(sprite, display_name, price, VS.getPlayer().getCredits(), item_name, message)
			else:
				self.drawBlank("NOTHING TO BUY")

		if self.state == "sell":
			if len(self.sell):
				item_name, damage, type, mount_num, quantity = self.sell[self.current_item]
				display_name = lookup_upgrade_name(item_name)
				if damage < 1.0:
					sprite       = lookup_upgrade_damaged_sprite(item_name)
				else:
					sprite       = lookup_upgrade_sprite(item_name)
				try:
					price = int( self.sell_prices[item_name] * damage )
				except:
					price = 0
				self.drawItem(sprite, display_name, price, VS.getPlayer().getCredits(), item_name, message, quantity, mount_num)
			else:
				self.drawBlank("NOTHING TO SELL")

		if self.state == "repair":
			if len(self.repair):
				player = VS.getPlayer()
				repair_index = self.repair[self.current_item]
				if repair_index >= 0:
					item_name, damage, type, mount_num, quantity = self.sell[repair_index]
					display_name = lookup_upgrade_name(item_name)
					sprite       = lookup_upgrade_damaged_sprite(item_name)
					# repair cost is the fraction of functionality * the repair_price
					try:
						price = int( self.repair_prices[item_name] * (1.0 - damage) )
					except:
						try:
							price = int( self.buy_prices[item_name] * (1.0 - damage) )
						except:
							price = 99999 # just some arbitrary large number
#				else:
#					item_name    = "basic_inspection"
#					display_name = item_name.title()
#					sprite       = lookup_upgrade_damaged_sprite(item_name)
#					global basic_repair_price
#					global basic_repair_cost
#					price = basic_repair_price * basic_repair_cost
#					mount_num = None

				self.drawItem(sprite, display_name, price, player.getCredits(), item_name, message, None, mount_num)
			else:
				self.drawBlank("NOTHING TO REPAIR")

	def drawItem(self, spr_file, name, cost, credits, item_name, message=None, quantity=None, mount=None):
		if mount == None:
			self.txt_name.setText( name )
		else:
			self.txt_name.setText( "%s (mount %s)" %(name, mount + 1) )
		self.txt_cost.setText( "Cost: %s" %(cost) )
		self.txt_credits.setText( "Credits: %s" %(int(credits)) )
		if (spr_file == ''):
			self.img_item.hide()
		else:
			self.img_item.setSprite( (spr_file, self.img_item_rect) )
			self.img_item.show()
		if message==None:
			self.txt_message.setText('')
		else:
			self.txt_message.setText(message)
		if quantity==None:
			self.txt_quantity.setText('')
		else:
			self.txt_quantity.setText( "Quantity: %s" %(quantity) )


	def drawBlank(self,message=None):
		self.txt_name.setText('')
		self.txt_cost.setText('')
		self.txt_credits.setText('')
		self.txt_quantity.setText('')
		self.img_item.hide()
		if message==None:
			self.txt_message.setText('')
		else:
			self.txt_message.setText(message)


def handle_RepairBayComputer_message(local, cmd, args, id):
	cp = VS.getCurrentPlayer()
	if VS.isserver():
		import server
		player = server.getDirector().getPlayer(cp)
		if not player.repair_bay_computer:
			player.repair_bay_computer = RepairBayComputerGeneric()
			if args[0] == "reload":
				return ["success", "loaded"]
		return player.repair_bay_computer.handle_server_cmd(args)
	elif RepairBayComputer.singleton:
		return RepairBayComputer.singleton.handle_server_cmd(args)
	else:
#		print "RepairBayComputer has no singleton!"
		print ("RepairBayComputer has no singleton!")
	return ["failure", 'RepairBayComputer has no singleton!']

custom.add("RepairBayComputer", handle_RepairBayComputer_message)

def handle_removeWeapon_message(local, cmd, args, id):
	VS.getPlayer().removeWeapon(args[0], int(args[1]), False)

custom.add("removeWeapon", handle_removeWeapon_message)

#
# helper functions used to add, remove, and repair various ship upgrades
#
def repair_item_cargo(player, item_name, count=1):
	if player.hasCargo(item_name):
		cargo_obj = player.GetCargo(item_name)
		# addCargo appears to append [count] items to current quantity, so we have to remove them first
		player.removeCargo(item_name,count,True)
		cargo_obj.SetFunctionality( cargo_obj.GetMaxFunctionality() )
		rc = player.addCargo(cargo_obj)
		if rc: return True
	return False

def repair_item(player, item_name, count=1):
	if player.hasCargo(item_name):
		cargo_obj = player.GetCargo(item_name)
		price     = cargo_obj.GetPrice()
		count     = cargo_obj.GetQuantity()
		# addCargo appears to append [count] items to current quantity, so we have to remove them first
		rc = player.removeCargo(item_name,count,True)
		if rc:
			return add_item(player, item_name, price, count)
		else:
#			print "removeCargo in repair_item failed: %s = player.removeCargo(%s, %s, %s)" (rc,item_name,count,True)
			print ("removeCargo in repair_item failed: %s = player.removeCargo(%s, %s, %s)",rc,item_name,count,True)
			return False

def add_item_cargo(player, item_name, price, count=1):
	global master_part_list
	mpl = master_part_list.getEntry(item_name)
	try:
		category = mpl.GetCategory()
		mass     = mpl.GetMass()
		volume   = mpl.GetVolume()
		func     = mpl.GetMaxFunctionality()
	except:
		category = "upgrades/Miscellaneous"
		mass     = 0.01
		volume   = 1.0
		func     = 1.0
	#    VS.Cargo __init__ appears to use: Content, Category, Price, Quantity, Mass, Volume
	cargo_obj = VS.Cargo(item_name, category, price, count, mass, volume)
	cargo_obj.SetMaxFunctionality(func)
	cargo_obj.SetFunctionality(func)
	rc = player.addCargo(cargo_obj)
	if rc: return True
	return False

def add_item(player, item_name, price, count=1, force=0):
	mount_num = 0 # player.getNumMounts()
	subunit_num = 0
	# calling Unit.upgrade with jump_drive, aftreburner etc returns 0.0, so add_upgrade returns False.
	# just assume it worked, and call add_item_cargo
	add_upgrade(player, item_name, mount_num, subunit_num, force, 0)
	rc = add_item_cargo(player, item_name, price, count)
	return rc

def remove_item_cargo(player, item_name, count=1):
	if player.hasCargo(item_name):
		rc = player.removeCargo(item_name,count,True)
		if rc: return True
	return False

def remove_item(player, item_name, count=1, recompute=True):
	rc = remove_item_cargo(player, item_name, count)
	# note: this takes the place of a player.downgrade(item_name) function
	# rather than remove only the item, it starts from the ship blank, and 
	# re-adds all the upgrades
	# because of the way this works, player should do the basic upgrade first
	if recompute:
		player.RecomputeUnitUpgrades()
	return rc


def repair_upgrade(player, item_name, mount_num=0, subunit_num=0):
	#    remove then re-add the item
	if (item_name != 'missile_launcher') and (item_name != 'torpedo_launcher'):
		remove_upgrade(player, item_name, mount_num)
	return add_upgrade(player, item_name, mount_num, subunit_num, 1)

def add_upgrade(player, item_name, mount_num=0, subunit_num=0, force=0, loop=0):
	#    Unit.upgrade parameters: string file,int mountoffset,int subunitoffset, bool force,bool loop_through_mounts
	rc = player.upgrade(item_name, mount_num, subunit_num, force, loop)
	if rc > 0:
		return True
	return False

def remove_upgrade(player, item_name, mount_num):
	# Unit.removeWeapon uses the names from weapons.xml, not from units.csv or master_part_list.csv....
	weapon_name = lookup_weapon_name(item_name)
	# the boolean value in removeWeapon parameters does nothing, btw
	if (player.removeWeapon(weapon_name, mount_num, False)!=-1):
		# This function doesn't run over network in C++
		if VS.isserver():
			custom.run("removeWeapon", [weapon_name, mount_num], None, None,
				player.isPlayerStarship())
		return True
	return False

def add_turret(player, item_name, force=0):
	if item_name == "medium_turret_bottom_meson":
		item_name = "medium_turret_meson"
		subunit_num = 1
	else:
		subunit_num = 0
	return add_upgrade(player, item_name, 0, subunit_num, force, 0)

def remove_turret(player, item_name):
	# removing a turret means installing a blank turret
	if item_name == "medium_turret_bottom_meson":
		item_name = "medium_turret_blank"
		subunit_num = 1
	elif item_name == "medium_turret_meson":
		item_name = "medium_turret_blank"
		subunit_num = 0
	else:
		item_name = "medium_turret_rear_blank"
		subunit_num = 0
	return add_upgrade(player, item_name, 0, subunit_num, 0, 0)

def repair_turret(player, item_name):
	# just reinstall the current turret
	return add_turret(player, item_name, 1)

def available_mounts(mounts, which, couldBeTractor=True):
#	print "available?"
#	print mounts
	print ("available?")
	print (mounts)
	new_list = []
	try:
		slots = mounts[which]
	except:
		return new_list
	for i in range(len(slots)):
		mount_num = slots[i]
		try:
			if (mounts['empty'][mount_num] and (not mount_num in mounts['torpedo']) and (not mount_num in mounts['missile'])):
				new_list.append(mount_num)
		except:
			pass
#	print "new listed "+which
#	print new_list
	print ("new listed "+which)
	print (new_list)
	if len(new_list)==0 and which=='special' and couldBeTractor:#go through again looking for empty missile launchers
		new_list=available_missile_mounts(mounts,'missile','blargh')+available_missile_mounts(mounts,'torpedo','blargh')
#		for i in range(len(slots)):
#			mount_num = slots[i]
#			try:
#				if (mounts['empty'][mount_num]):
#					new_list.append(mount_num)
#			except:
#				pass
#		print "new new list"
#		print new_list
		print ("new new list")
		print (new_list)
	return new_list

def available_missile_mounts(mounts, which, item_name):
	new_list = []
	try:
		slots = mounts[which]
	except:
		return new_list
	player = VS.getPlayer()
	for i in range(len(slots)):
		mount_num = slots[i]
		mount = player.GetMountInfo(mount_num)
		count = mount['ammo']
		max   = mount['volume']
		empty = mount['empty']
		if empty or (count == 0):
			# empty
			new_list.append(mount_num)
		elif (count == max):
			# full
			pass
		else:
			# partially full
			try:
				name = lookup_item_name( mount['weapon_info']['name'] )
			except:
				name = ''
			if (item_name == name):
				new_list.append(mount_num)
	return new_list


#
# helper functions used by Software Booth
#	add_map
#	remove_map
#	has_map
#
def add_map(map_id):
	# farris should be spelled Fariss, but user doesn't see this value
	cp = VS.getCurrentPlayer()
	if map_id=='farris_map':
		quest.removeQuest(cp,map_id,1.0)
		quest.removeQuest(cp,"visited_Gemini/17-ar",1.0)
		quest.removeQuest(cp,"visited_Gemini/Capella",1.0)
		quest.removeQuest(cp,"visited_Gemini/Castor",1.0)
		quest.removeQuest(cp,"visited_Gemini/Crab-12",1.0)
		quest.removeQuest(cp,"visited_Gemini/Death",1.0)
		quest.removeQuest(cp,"visited_Gemini/Famine",1.0)
		quest.removeQuest(cp,"visited_Gemini/J900",1.0)
		quest.removeQuest(cp,"visited_Gemini/KM-252",1.0)
		quest.removeQuest(cp,"visited_Gemini/New_Caledonia",1.0)
		quest.removeQuest(cp,"visited_Gemini/Nexus",1.0)
		quest.removeQuest(cp,"visited_Gemini/Palan",1.0)
		quest.removeQuest(cp,"visited_Gemini/Pestilence",1.0)
		quest.removeQuest(cp,"visited_Gemini/Regallis",1.0)
		quest.removeQuest(cp,"visited_Gemini/Rygannon",1.0)
		quest.removeQuest(cp,"visited_Gemini/Sherwood",1.0)
		quest.removeQuest(cp,"visited_Gemini/Telar",1.0)
		quest.removeQuest(cp,"visited_Gemini/Valhalla",1.0)
		quest.removeQuest(cp,"visited_Gemini/War",1.0)
		quest.removeQuest(cp,"visited_Gemini/Xyanti",1.0)
		# Fariss has several hidden systems, including Delta_Prime and Eden
	elif map_id=='clarke_map':
		quest.removeQuest(cp,map_id,1.0)
		quest.removeQuest(cp,"visited_Gemini/Blockade_Point_Alpha",1.0)
		quest.removeQuest(cp,"visited_Gemini/Blockade_Point_Charlie",1.0)
		quest.removeQuest(cp,"visited_Gemini/Blockade_Point_Tango",1.0)
		quest.removeQuest(cp,"visited_Gemini/CMF-A",1.0)
		quest.removeQuest(cp,"visited_Gemini/Hyades",1.0)
		quest.removeQuest(cp,"visited_Gemini/Lisacc",1.0)
		quest.removeQuest(cp,"visited_Gemini/Mah_Rahn",1.0)
		quest.removeQuest(cp,"visited_Gemini/Midgard",1.0)
		quest.removeQuest(cp,"visited_Gemini/Nitir",1.0)
		quest.removeQuest(cp,"visited_Gemini/Perry",1.0)
		quest.removeQuest(cp,"visited_Gemini/Ragnarok",1.0)
		quest.removeQuest(cp,"visited_Gemini/Rikel",1.0)
		quest.removeQuest(cp,"visited_Gemini/Sumn_Kpta",1.0)
		quest.removeQuest(cp,"visited_Gemini/Surtur",1.0)
		quest.removeQuest(cp,"visited_Gemini/Tingerhoff",1.0)
		quest.removeQuest(cp,"visited_Gemini/Tr_Pakh",1.0)
	elif map_id=='potter_map':
		quest.removeQuest(cp,map_id,1.0)
		quest.removeQuest(cp,"visited_Gemini/41-gs",1.0)
		quest.removeQuest(cp,"visited_Gemini/44-p-im",1.0)
		quest.removeQuest(cp,"visited_Gemini/Aldebran",1.0)
		quest.removeQuest(cp,"visited_Gemini/Auriga",1.0)
		quest.removeQuest(cp,"visited_Gemini/DN-N1912",1.0)
		quest.removeQuest(cp,"visited_Gemini/Hinds_Variable_N",1.0)
		quest.removeQuest(cp,"visited_Gemini/Manchester",1.0)
		quest.removeQuest(cp,"visited_Gemini/Metsor",1.0)
		quest.removeQuest(cp,"visited_Gemini/ND-57",1.0)
		quest.removeQuest(cp,"visited_Gemini/New_Constantinople",1.0)
		quest.removeQuest(cp,"visited_Gemini/New_Detroit",1.0)
		quest.removeQuest(cp,"visited_Gemini/Newcastle",1.0)
		quest.removeQuest(cp,"visited_Gemini/Oxford",1.0)
		quest.removeQuest(cp,"visited_Gemini/Raxis",1.0)
		quest.removeQuest(cp,"visited_Gemini/Saxtogue",1.0)
		quest.removeQuest(cp,"visited_Gemini/Shangri_La",1.0)
		quest.removeQuest(cp,"visited_Gemini/XXN-1927",1.0)
	elif map_id=='humboldt_map':
		quest.removeQuest(cp,map_id,1.0)
		quest.removeQuest(cp,"visited_Gemini/119ce",1.0)
		quest.removeQuest(cp,"visited_Gemini/CM-N1054",1.0)
		quest.removeQuest(cp,"visited_Gemini/Freyja",1.0)
		quest.removeQuest(cp,"visited_Gemini/Junction",1.0)
		quest.removeQuest(cp,"visited_Gemini/Padre",1.0)
		quest.removeQuest(cp,"visited_Gemini/Penders_Star",1.0)
		quest.removeQuest(cp,"visited_Gemini/Pentonville",1.0)
		quest.removeQuest(cp,"visited_Gemini/Pollux",1.0)
		quest.removeQuest(cp,"visited_Gemini/Prasepe",1.0)
		quest.removeQuest(cp,"visited_Gemini/Pyrenees",1.0)
		quest.removeQuest(cp,"visited_Gemini/Troy",1.0)
		quest.removeQuest(cp,"visited_Gemini/Varnus",1.0)
	else:
		# just add the map_id, so we can have other sectors if we want
		quest.removeQuest(cp,map_id,1.0)

def remove_map(map_id):
	cp = VS.getCurrentPlayer()
	# this appears to set the value, so I don't know why it's called 'removeQuest'
	quest.removeQuest(cp,map_id,0.0)

def has_map(map_id):
	return quest.checkSaveValue(VS.getCurrentPlayer(),map_id,1.0)


#
# make looking up part list category, price, etc easier
#
class MasterPartList:
	def __init__(self):
		self.list = {}
		master_list = VS.GetMasterPartList()

		for i in range(master_list.numCargo()):
			cargo = master_list.GetCargoIndex(i)
			name  = cargo.GetContent()
			self.list[name] = cargo

	def getRadarList(self):
		radar = []
		for name in self.list:
			cargo = self.list[name]
			category = cargo.GetCategory()
			if category[:14] != 'upgrades/Radar': continue
			radar.append(cargo)
		return radar	

	def getUpgradeList(self):
		upgrades = []
		for name in self.list:
			cargo = self.list[name]
			category = cargo.GetCategory()
			if category[:8]  != 'upgrades': continue
			if category[:14] == 'upgrades/Radar': continue
			upgrades.append(cargo)
		return upgrades	

	def getEntry(self, name):
		try:
			return self.list[name]
		except:
			return None

#
# ShipPurchase, BuyShip, et al
#	code called by Base.Python in MakeWeapon
#	this shows the ship dealer, checks if you can afford the ship model chosen, makes an offer, 
#	and completes the transaction if accepted
#
def ShipPurchase(shipname):
	import Base
	import VS
	import fixers
	import campaign_lib
	campaign_lib.AddConversationStoppingSprite("Ship_Dealer","bases/heads/shipdealer.spr",(.582,-.2716),(3.104,2.4832),"Return_To_Showroom").__call__(Base.GetCurRoom(),None)
	VS.StopAllSounds()
	if (VS.getPlayer().getName()==shipname or VS.getPlayer().getName()+".begin"==shipname or VS.getPlayer().getName()==shipname+".begin"):
		VS.playSound("sales/pitch"+shipname+"duplicate.wav",(0,0,0),(0,0,0))
	elif CanBuyShip(shipname+".begin"):
		fixers.CreateChoiceButtons(Base.GetCurRoom(),[
			fixers.Choice("bases/fixers/yes.spr","#\nimport fixers\nfixers.DestroyActiveButtons ()\nimport weapons_lib\nimport VS\nVS.StopAllSounds()\nweapons_lib.BuyShip('"+shipname+".begin')\n","Purchase "+shipname.capitalize()),
			fixers.Choice("bases/fixers/no.spr","#\nimport fixers\nfixers.DestroyActiveButtons ()\nimport VS\nVS.StopAllSounds()\nVS.playSound('sales/pitch"+shipname+"reject.wav',(0,0,0),(0,0,0))\n","Decline Purchasing")])
		VS.playSound("sales/pitch"+shipname+".wav",(0,0,0),(0,0,0))
	else:
		VS.playSound("sales/pitchnotenoughmoney.wav",(0,0,0),(0,0,0))
		Base.Message("I hate to break it to you, but we've checked your account, and you don't have enough credits to buy this ship. She sure is a fine ship though, isn't she? Listen, I want to make a sale, you want to make a purchase, lets look at the facts. You know the retail of this ship--we can use your ship for tradeins, plus extras--including your cash on hand, that still leaves you short.  Go get some more cash, and come back when you have more cash, and don't feel embarrassed: these things happen!")
def ShipValue(shipname, used):
	import VS
	carg=VS.GetMasterPartList().GetCargo(shipname)
	price=carg.GetPrice()
	if used:
		try:
			price*=float(VS.vsConfig("economics","ship_sellback_price",".5"))
		except:
			price*=.5
	return price
def CargoValue(un):
	numcarg=un.numCargo()
	tot=0
	for i in range(numcarg):
		c=un.GetCargoIndex(i)
		if c.GetCategory().find("upgrades")==0:
			tot+=c.GetPrice()*c.GetQuantity()*.5
	return tot;
def CanBuyShip(shipname):
	import VS
	creds=VS.getPlayer().getCredits()
	return creds+ShipValue(VS.getPlayer().getName(),True)+CargoValue(VS.getPlayer())>=ShipValue(shipname,False)
def BuyShip(shipname):
	# set the basic_repair_cost to 0
#	global basic_repair_cost
#	basic_repair_cost = 0
	# sell off the old ship and buy a new one
	import VS
	import Base
	name=VS.getPlayer().getName()
	value=CargoValue(VS.getPlayer())+ShipValue(name,True)
	oldcargo=[]
	oldun=VS.getPlayer()
	for i in range(oldun.numCargo()):
		c=oldun.GetCargoIndex(i)
		if c.GetCategory().find("upgrades")!=0:
			oldcargo.append(c)
	#print value
	#print VS.getPlayer().getCredits()
	VS.getPlayer().addCredits(value)
	success=Base.BuyShip(shipname,False,True)
	if (success!=False):
		Base.SellShip(name)
		#print VS.getPlayer().getCredits()
		#VS.getPlayer().addCredits(-ShipValue(shipname,False))
		#print VS.getPlayer().getCredits()
		#for carg in oldcargo:
		#	VS.getPlayer().addCargo(carg)
		where=shipname.find(".begin")
		if (where!=-1):
			shipname=shipname[0:where]
		VS.StopAllSounds()
		VS.playSound('sales/pitch'+shipname+'accept.wav',(0,0,0),(0,0,0))
# unneeded because of PlayerShip.RefreshPlayerShips()
#		Shipname=shipname.capitalize()
#		Base.EraseObj(0,'landship')
#		print "erased landship"
#		print 'bases/'+basename+"/LandingBay_"+Shipname+".spr"
#		Base.Texture(0,'landship','bases/'+basename+"/LandingBay_"+Shipname+".spr",0,0)
		PlayerShip.RefreshPlayerShips()
		return True
	else:
		where=shipname.find(".begin")
		if (where!=-1):
			shipname=shipname[0:where]
		VS.StopAllSounds()
		VS.playSound("sales/pitch"+shipname+"duplicate.wav",(0,0,0),(0,0,0))		
		return False


# global variables
master_part_list   = MasterPartList()
#basic_repair_price = 100
#basic_repair_cost  = 0
basename="perry"
