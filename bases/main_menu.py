import dj_lib

dj_lib.disable()
import Base
import VS
import GUI
import ShowProgress

import computer_lib

def StartNewGame(self,params):
	ShowProgress.activateProgressScreen('loading',3)
	VS.loadGame(VS.getNewGameSaveName())

def QuitGame(self,params):
	Base.ExitGame()

# this uses the original coordinate system of Privateer
GUI.GUIInit(320,200)

time_of_day=''

# Base music
plist_menu=VS.musicAddList('maintitle.m3u')
plist_credits=VS.musicAddList('maincredits.m3u')

def enterMainMenu(self,params):
	global plist_menu
	VS.musicStop()
	VS.musicPlayList(plist_menu)

def enterCredits(self,params):
	global plist_credits
	VS.musicStop()
	VS.musicPlayList(plist_credits)

# Create menu room
#room_intro = Base.Room ('XXXIntro')
room_menu = Base.Room ('XXXMain_Menu')
guiroom  = GUI.GUIRoom(room_menu)

# Set up intro room
#class IntroRoom(GUI.GUIMovieRoom):
#    def onStart(self, video):
#        Base.SetDJEnabled(0)
#        GUI.GUIMovieRoom.onStart(self, video)
#    def onSkip(self, button, params):
#        global starting_new_game, plist_monologue
#        IntroRoom.onSkip(self, button, params)
        #DoStartNewGame(self, params)
#        starting_new_game = True
#        VS.musicPlayList(plist_monologue)
#        Base.SetCurRoom(intro_guiroom.getIndex())

#Uncomment the following lines to use intro movies
#introroom = IntroRoom(room_intro,
#    ( 'intro.avi',
#      GUI.GUIRect(0, 0, 1, 1, "normalized")),
#    guiroom)
#introroom.setAspectRatio(16.0/9.0)

# Create credits room
credits_guiroom = GUI.GUIRoom(Base.Room('XXXCredits'))
GUI.GUIStaticImage(credits_guiroom, 'background', ( 'interfaces/main_menu/credits.spr', GUI.GUIRect(0, 0, 1024, 768, "pixel", (1024,768)) ))

# Button to go back to the main menu (from the credits)
sprite_loc = GUI.GUIRect(32,697,482,47,"pixel",(1024,768))
sprite = {
	'*':None,
	'down' : ( 'interfaces/main_menu/credits_resume_button_pressed.spr', sprite_loc ) }
GUI.GUIRoomButton (credits_guiroom, guiroom, 'XXXMain Menu','Main_Menu',sprite,sprite_loc,clickHandler=enterMainMenu)


# Create background
GUI.GUIStaticImage(guiroom, 'background', ( 'interfaces/main_menu/menu.spr', GUI.GUIRect(0, 0, 1024, 768, "pixel", (1024,768)) ))

# Create the Quine 4000 screens
rooms_quine = computer_lib.MakePersonalComputer(room_menu, room_menu,
	0, # do not make links
	0, 0, 0, # no missions, finances or manifest
	1, # do enable load
	0, # but disable save
	1) # and return room map, rather than only root room
rooms_quine['computer'].setMode('load')

# Link to Quine "Load Game" screen
sprite_loc = GUI.GUIRect(272,697,241,47,"pixel",(1024,768))
sprite = {
	'*':None,
	'down' : ( 'interfaces/main_menu/load_button_pressed.spr', sprite_loc ) }
GUI.GUIRoomButton(guiroom, rooms_quine['load'], 'XXXLoad Game','Load_Game',sprite,sprite_loc)

# Link to Credits or Network Setup
sprite_loc = GUI.GUIRect(513,697,241,47,"pixel",(1024,768))
sprite = {
	'*':None,
	'down' : ( 'interfaces/main_menu/credits_button_pressed.spr', sprite_loc ) }
#GUI.GUICompButton(guiroom,'Network','XXXPlay Network','Network_Game',sprite,sprite_loc)		# network game setup
GUI.GUIRoomButton(guiroom, credits_guiroom, 'XXXShow Credits','Show_Credits',sprite,sprite_loc,clickHandler=enterCredits)	# credits screen

# New game
sprite_loc = GUI.GUIRect(31,697,241,47,"pixel",(1024,768))
sprite = {
	'*':None,
	'down' : ( 'interfaces/main_menu/new_button_pressed.spr', sprite_loc ) }
btn = GUI.GUIButton(guiroom, 'XXXNew Game','New_Game',sprite,sprite_loc,'enabled',StartNewGame)

# Quit game
sprite_loc = GUI.GUIRect(753,697,241,47,"pixel",(1024,768))
sprite = {
	'*':None,
	'down' : ( 'interfaces/main_menu/quit_button_pressed.spr', sprite_loc ) }
btn = GUI.GUIButton(guiroom, 'XXXQuit Game','Quit_Game',sprite,sprite_loc,'enabled',QuitGame)

# Draw everything
GUI.GUIRootSingleton.broadcastMessage('draw',None)

# Base music
VS.musicStop()
VS.musicPlayList(plist_menu)

