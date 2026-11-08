"""Start the privateer() dynamic universe (random encounters, traffic, dynamic
missions) for a game that is being loaded.

The New_Game save, and saves written before the dynamic universe was hooked up,
do not list it in their active missions, so nothing would ever spawn. Saves made
since then do list it, and the engine's LoadSavedMissions restarts it from there;
queuing a second copy would double the traffic.

The mission is queued with DelayLoadMission rather than loaded immediately: the
engine starts delayed missions only after the queued game load has happened, so
the new game's LoadSavedMissions cannot terminate it. It is a named persistent
script, so it is written into the save's active scripts from then on.
"""
import os
import VS

UNIVERSE_MISSION = '#privateer_universe'
UNIVERSE_SCRIPT = ('from privateer import privateer\n'
                   'my_obj=privateer(3000,5000,500,3,2,.6,.25,.1,850000,2000)\n')


def save_has_universe(savename):
    path = os.path.join(VS.getSaveDir(), savename)
    try:
        with open(path, 'r', encoding='latin-1') as f:
            return UNIVERSE_MISSION[1:] in f.read()
    except OSError:
        return False


def start_unless_saved(savename):
    if savename and save_has_universe(savename):
        return
    try:
        VS.DelayLoadMission(UNIVERSE_MISSION, UNIVERSE_SCRIPT)
    except Exception as e:
        print('Could not queue privateer dynamic universe: %r' % (e,))
