import custom
import debug
import dialog_box
import VS


class StringWriter:
	def __init__(self,orig=''):
		self.text=orig
	def write(self, text):
		self.text += text
	def __str__(self):
		return self.text
	


def runAdminMenu(cp=-1, local=False):
	items=['position', 0, 0.6, 
		'width', 1.25,
		'row',
		'textwidth','Command:',0.3,
		'textinput','cmd','',
		'col','width',0.2,'button','Clear','endcol'
		'endrow']
	items += dialog_box.button_row(1.25, 'Enter', 'Cancel')
	def callback(dialog, result):
		action,inputs = dialog_box.fromValues(result)
		cmd = inputs['cmd']
		if action=='Cancel':
			dialog.undraw()
			custom.respond(['close'],None,id)
			return False
		elif action=='Clear' or cmd=='':
			#dialog.undraw()
			#custom.respond(['close'],None,id)
			#runServerMenu(cp, local)
			#return False
			custom.respond(['reset'],None,id)
		elif action=='Enter' or action=='OK':
			if cmd.find(' ')==-1:
				cmd = cmd + ' '
			if cmd[0]=='/':
				cmd = cmd[1:]
			command, argstr = cmd.split(' ',1)
			dialogWriter = StringWriter('Response to previous command:\n')
			ret = custom.processMessage(local, command, argstr, 'null', dialogWriter)
			output = str(dialogWriter)
			if ret:
				output += "\n"+(": ".join(output))
			dialog_box.alert(output, buttonText='Close', y=-.02)
		return True
	id = dialog_box.dialog(items,callback)

def runBountyMenu(cp=-1):
	if cp==-1:
		cp=VS.getCurrentPlayer()
	un = VS.getPlayerX(cp)
	id=None
	
	def callback(dialog,result):
		print ('id is: ',id)
		action,inputs = dialog_box.fromValues(result)
		if action=='Cancel':
			dialog.undraw()
			custom.respond(['close'],None,id)
			return False
		if action=='OK':
			dialog.undraw()
			custom.respond(['close'],None,id)

			callsign = inputs['logged_in_users']
			if callsign=='' or callsign=='OR, Type in a user:':
				callsign = inputs['callsign']

			print ('I would now place a bounty on '+str(callsign)+' for '+str(float(inputs['credits']))+' credits.')
			print ('User value IS: '+str(inputs['logged_in_users']))
			return False
		return True
	
	items=['width', 1.5,
		'text', "Place a bounty on someone's head",
]
	items+=['height',0.05,
		'row',
		'textwidth','Credits:',0.3,
		'textinput','credits',un.getCredits(),
		'endrow',
		'height',0.05]
	if VS.isserver():
		import server
		logged_in_users=server.getDirector().getCallsignList()
		logged_in_users.append('OR, Type in a user:')
		items+=['text','Select a player in this system:',
			'list','logged_in_users',len(logged_in_users)]+logged_in_users
		items+=['row',
			'textwidth','Other Player:',0.3,
			'textinput','callsign','',
			'endrow']
	else:
		items+=['list','logged_in_users',15,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
	items += dialog_box.button_row(1.5,'OK','Cancel')
	id = dialog_box.dialog(items,callback)
	

def runComputer(local,cmd,args,id,cp=-1):
	#def a():
	#	print ("A() called")
	#	def b(result):
	#		print (result)
	#		if not result:
	#			result='NOT'
	#		def c(result):
	#			dialog_box.alert(result)
	#		dialog_box.confirm("Test message 2 "+str(result),c)
	#	dialog_box.confirm("Test message",b,buttons=('A','B','C','D','E',"F",'G','H','I','J'))
	#dialog_box.alert("TEST\nALERT\nBox",callback=a)
	if cp == -1:
		cp = VS.getCurrentPlayer()
	player=None
	room1 = -1
	if len(args)>=1:
		room1 = args[0]
	room2 = -1
	if len(args)>=2:
		room2 = args[1]
	if VS.isserver():
		import server
		player = server.s().getPlayer(cp)
	if player and player.computer_open:
		debug.debug("Computer already open")
		return
	
	def callback(dialog,result):
		print ('id is: ',id)
		action,inputs = dialog_box.fromValues(result)
		if action=='Save Game':
			dialog_box.confirm("Really Save?", lambda bool:bool and VS.saveGame(str(cp)))
		if action=='Die and Reload':
			dialog_box.confirm("Really Commit Suicide?", lambda bool:bool and VS.loadGame(str(cp)))
		if action=='Server Admin':
			runAdminMenu(cp, local)
		if action=='Bounty Hunt':
			print ('hunting bounty')
			runBountyMenu(cp)
		if action=='OK' or action=="Exit Menu" or action=="Cancel" or action=="Open Quine":
			if player:
				player.computer_open = False
			dialog.undraw()
			custom.respond(['close'],None,id)
			return False
		return True
	
	items=['width', 1.0,
		'text', 'Public Computer Menu',
		'space', 0., .1,
		'button', 'Save Game',
		'button', 'Die and Reload',
		'button', 'Server Admin',
		'button', 'Bounty Hunt']
	if room2>=0:
		items += ['room', room2, 'Open Quine']
	items += ['room', room1, 'Exit Menu']
	id = dialog_box.dialog(items,callback)
	if player:
		player.computer_open = True

custom.add("computer",runComputer)

