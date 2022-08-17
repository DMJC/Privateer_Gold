import Base
import VS

config_map = {}
active_list = []

def RegisterPlayerShipSet(setname,setmap):
	config_map[setname] = setmap

def InitPlayerShips():
	global active_list
	active_list = []

def RefreshPlayerShips():
	for i in range(len(active_list)):
		RefreshPlayerShip(i)

def RefreshPlayerShip(which):
	ship = VS.getPlayer().getName()
	set = active_list[which][0]
	room = active_list[which][1]
	index = active_list[which][2]
	config = config_map[set]
	if active_list[which][3]:
		Base.EraseObj(room,index)
		active_list[which] = (set,room,index,0,0)
	for i in config:
		if (i != '*3D*') and (ship.find(i)==0) and (len(config[i]) >= 3):
			# Found a sprite-based entry
			sprite = config[i]
			Base.Texture(room,index,sprite[0],sprite[1],sprite[2])
			active_list[which] = (set,room,index,1,(i,sprite));
			break
	if (active_list[which][3]==0) and ('*3D*' in config) and (len(config['*3D*'])>=3):
		# No sprite-based entry - create a 3D entry
		Base.Ship (room, index, config['*3D*'][0], config['*3D*'][1], config['*3D*'][2])
		active_list[which] = (set,room,index,1,0)
	elif (active_list[which][3]==0):
		# Bummer...
#		print "* PlayerShip: No match found for ship " + ship + "\n"
		print ("* PlayerShip: No match found for ship " + ship + "\n")
		active_list[which] = (set,room,index,0,0)

def AddPlayerShips(set,room,index):
	if (set in config_map):
		# Add uninitialized entry, and refresh it to initialize
		active_list.append( (set,room,index,0,0) )
		RefreshPlayerShip(len(active_list)-1)


from PlayerShip_config import autoregister_map

for i in autoregister_map:
	RegisterPlayerShipSet(i,autoregister_map[i])

