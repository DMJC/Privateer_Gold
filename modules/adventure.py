import quest
import quest_drone
import vsrandom
import quest_surplus
import VS
#VS is only for news

adventures = {}

persistent_adventures = list()

adventures = {
	"Gemini/Delta_Prime":quest_drone.quest_drone_factory(),
#	"Enigma/callimanchius":quest_surplus.quest_surplus_factory(('Supplies/Medical','Research/Environmental',),1.5,.5,0,1,('callimanchius_disaster',),),
#	"Sol/alpha_centauri":quest_surplus.quest_surplus_factory(('Supplies/Construction_Supplies','Manufactured_Goods',),1.5,.5,0,1,('holman_population',),),
	}
persistent_adventures = [
	quest_drone.quest_drone_factory(),
	]

def removePersistentAdventure(newq):
    mylen = len(persistent_adventures)
    if (mylen):
        for x in range (mylen):
            if (persistent_adventures[x]==newq):
                del persistent_adventures[x]
                return

def newAdventure(playernum,oldsys,newsys):
    newfac=adventures.get (newsys)
    if (newfac):
        newq = newfac.factory(playernum)
        if (newq):#only remove it if that player hasn't done it before
            del adventures[newsys]
            removePersistentAdventure(newfac)
        return newq
    return
#that returns false

def persistentAdventure(playernum):
    for index in range (len(persistent_adventures)):
        ret = persistent_adventures[index].persistent_factory(playernum)
        if (ret):
            del persistent_adventures[index]
            return ret
    if (0 and vsrandom.randrange(0,4)==0):
        (key,val,news)=quest_surplus.makeSurplusShortage()
        if (not adventures.get(key)):
            adventures.setdefault(key,val)
            VS.IOmessage (0,"game","news",news)
    return
