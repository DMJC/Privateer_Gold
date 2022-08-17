import Base
import VS
import GUI

import dj_lib
dj_lib.disable()

def RestartGame(self,params):
	VS.loadGame(VS.getCurrentSaveGame())

def QuitGame(self,params):
	Base.ExitGame()

# All interface art for this script was natively rendered on 1024x768
GUI.GUIInit(1024,768)

time_of_day=''

# Create menu room
room_menu = Base.Room ('XXXDeath_Menu')
guiroom  = GUI.GUIRoom(room_menu)

# Create background
GUI.GUIStaticImage(guiroom, 'background', ( 'interfaces/death_menu/menu.spr', GUI.GUIRect(0, 0, 1024, 768, "pixel") ))


# Button to go back to the last save game
sprite_loc = GUI.GUIRect(32,697,482,47,"pixel")
sprite = {
	'*':None,
	'down' : ( 'interfaces/death_menu/restart_button_pressed.spr', sprite_loc ) }
GUI.GUIButton (guiroom, 'XXXRestart','Restart',sprite,sprite_loc,clickHandler=RestartGame)

# Button to go back to the last save game
sprite_loc = GUI.GUIRect(514,697,482,47,"pixel")
sprite = {
	'*':None,
	'down' : ( 'interfaces/death_menu/quit_button_pressed.spr', sprite_loc ) }
GUI.GUIButton (guiroom, 'XXXRestart','Restart',sprite,sprite_loc,clickHandler=QuitGame)

# Draw everything
GUI.GUIRootSingleton.broadcastMessage('draw',None)

