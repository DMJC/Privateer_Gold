import VS
import Director
import fg_util
import vsrandom
import faction_ships
import universe
import dynamic_universe
import dynamic_news
import debug
import generate_dyn_universe
import PickleTools
global dnewsman_
dnewsman_ = dynamic_news.NewsManager()
baseship=None
plr=0
basefac='neutral'

mission_script_template = '''
import mission_lib
import %(module)s
temp=%(module)s.%(constructor)s%(args)r
mission_lib.AddMissionHooks(temp)
temp=0
'''

# load the company names & briefing text from files only once
company_names = []
cargo_briefs  = []
attack_briefs = []
patrol_briefs = []
defend_briefs = []
escort_briefs = []
rescue_briefs = []
bounty_briefs = []

def formatShip(ship):
    where=ship.find(".blank")
    if (where!=-1):
        ship=ship[0:where]
    return ship.capitalize()

def formatCargoCategory(ship):
    where=ship.rfind("/")
    if (where!=-1):
        ship=ship[where+1:]
    return ship.capitalize()

#Credit to Peter Trethewey, master of python and all things nefarious
def getSystemsKAwayNoFaction( start, k ):
    set = [start]#set of systems that have been visited
    pathset = [[start]]#parallel data structure to set, but with paths
    pathtor = [[start]]#parallel data structure to raw return systems with path
    r = [start] #raw data structure containing systems n away where n<=k
    for n in range(0,k):
        set.extend(r)
        pathset.extend(pathtor)
        r=[]
        pathtor=[]
        for iind in range(len(set)):
            i = set[iind]
            l = universe.getAdjacentSystemList(i)
            for jind in range(len(l)):
                j=l[jind]
                if not (j in set or j in r):
                    r.append(j)
                    pathtor.append(pathset[iind]+[j])
    return pathtor

def getSystemsNAway (start,k,preferredfaction):
    l = getSystemsKAwayNoFaction(start,k)
    if (preferredfaction==None):
        return l
    lbak=l
    if (preferredfaction==''):
        preferredfaction=VS.GetGalaxyFaction(start)
    i=0
    while i <len(l):
        if (VS.GetRelation(preferredfaction,VS.GetGalaxyFaction(l[i][-1]))<0):
            del l[i]
            i-=1
        i+=1
    if (len(l)):
        return l
    return lbak

syscreds=750

def LoadList(filename):
	bnl = []
	print ('Importing list from: ' + filename)
	try:
		f = open (filename,'r')
		bnl = f.readlines()
		f.close()
	except:
		return []
	# strip newlines
	for i in range(len(bnl)):
		bnl[i]=bnl[i].rstrip()
	return bnl

def GetRandomFromList(list):
	import vsrandom
	idx = vsrandom.randint(0,len(list)-1)
	return list[idx]

def GetRandomCompanyName():
	#print ('reading company names ')
	global company_names
	if (len(company_names) == 0):
		filename = 'universe/companies.txt'
		company_names = LoadList(filename)
	return GetRandomFromList(company_names)

def GetRandomCargoBrief():
	#print ('generating cargo briefing')
	global cargo_briefs
	if (len(cargo_briefs) == 0):
		filename = 'universe/cargo_brief.txt'
		cargo_briefs = LoadList(filename)
	return GetRandomFromList(cargo_briefs)

def GetRandomAttackBrief():
	#print ('generating attack briefing')
	global attack_briefs
	if (len(attack_briefs) == 0):
		filename = 'universe/attack_brief.txt'
		attack_briefs = LoadList(filename)
	return GetRandomFromList(attack_briefs)

def numPatrolPoints(sysname):
    try:
        import faction_ships
        mmax=faction_ships.numPatrolPoints[sysname]
        # print ("system max "+sysname+" "+str(mmax))
        return vsrandom.randrange(4,mmax+1)
    except:
        return vsrandom.randrange(4,10)

def GetRandomPatrolBrief():
	#print ('generating patrol briefing')
	global patrol_briefs
	if (len(patrol_briefs) == 0):
		filename = 'universe/patrol_brief.txt'
		patrol_briefs = LoadList(filename)
	return GetRandomFromList(patrol_briefs)

def GetRandomDefendBrief():
	#print ('generating defend briefing')
	global defend_briefs
	if (len(defend_briefs) == 0):
		filename = 'universe/defend_brief.txt'
		defend_briefs = LoadList(filename)
	return GetRandomFromList(defend_briefs)

def GetRandomEscortBrief():
	#print ('generating escort briefing')
	global escort_briefs
	if (len(escort_briefs) == 0):
		filename = 'universe/escort_brief.txt'
		escort_briefs = LoadList(filename)
	return GetRandomFromList(escort_briefs)

def GetRandomRescueBrief():
	#print ('generating rescue briefing')
	global rescue_briefs
	if (len(rescue_briefs) == 0):
		filename = 'universe/rescue_brief.txt'
		rescue_briefs = LoadList(filename)
	return GetRandomFromList(rescue_briefs)

def GetRandomBountyBrief():
	#print ('generating bounty briefing')
	global bounty_briefs
	if (len(bounty_briefs) == 0):
		filename = 'universe/bounty_brief.txt'
		bounty_briefs = LoadList(filename)
	return GetRandomFromList(bounty_briefs)

def getCargoName(category):
    l=category.split('/')
    if len(l)>1:
        cargo = l[len(l)-1]+' '+l[0]
    else:
        cargo = category
    cargo = cargo.replace('_',' ')
    return cargo


def getMissionDifficulty ():
    import difficulty
    tmp=difficulty.getPlayerUnboundDifficulty(VS.getCurrentPlayer())
    if (tmp>1.5):
        tmp=1.5
    return tmp

def getPriceModifier(isUncapped):
    return 1.15
    import difficulty
    if (not difficulty.usingDifficulty()):
        return 1.0
    if (isUncapped):
        return getMissionDifficulty()/.5+.9
    return VS.GetDifficulty()/.5+.9

def howMuchHarder(makeharder):
    import difficulty
    if  (makeharder==0):
        return 0
    udiff = getMissionDifficulty()
    if (udiff<=1):
        return 0
    return int(udiff*2)-1

def processSystem(sys):
    k= sys.split('/')
    if (len(k)>1):
        k=k[1]
    else:
        k=k[0]
    return k
totalMissionNumber=0
insysMissionNumber=0
def checkInsysNum():
    global insysMissionNumber
    if insysMissionNumber:
        insysMissionNumber=0
        return True
    return False
def checkMissionNum():
    global totalMissionNumber
    if totalMissionNumber:
        totalMissionNumber=0
        return True
    return False
def checkCreatedMission():
    if (checkMissionNum()+checkInsysNum()>0):
        return True
    return False
def isFixerString(s):
    k=str(s)
    if (len(k)<2):
        return 0
    if (k[1]=='F'):
        return 1
    if (k[1]=='G'):
        return 2
    return 0
def writemissionname(name,path,isfixer):
    if (isfixer==0):
        if path[-1]==VS.getSystemFile():
            name="In_System_"+name
            global insysMissionNumber
            insysMissionNumber+=1
        else:
            global totalMissionNumber
            totalMissionNumber+=1
    Director.pushSaveString(plr, "mission_names", name)

    
def writedescription(name):
    Director.pushSaveString(plr, "mission_descriptions", name.replace("_"," "))
def writemissionsavegame (name):
    Director.pushSaveString(plr, "mission_scripts", name)
def writemissionvars (vars):
    Director.pushSaveString(plr, "mission_vars", PickleTools.encodeMap(vars))
def eraseExtras():
	Director.clearSaveString(plr, "mission_scripts")
	Director.clearSaveString(plr, "mission_names")
	Director.clearSaveString(plr, "mission_descriptions")
	Director.clearSaveString(plr, "mission_vars")

def eraseExtrasOld():
    import sys
    len=Director.getSaveStringLength(plr, "mission_scripts")
    if (   len!=Director.getSaveStringLength(plr, "mission_names") \
        or len!=Director.getSaveStringLength(plr, "mission_descriptions") \
        or len!=Director.getSaveStringLength(plr, "mission_vars")   ):
        sys.stdout.write("Warning: Number of mission descs., names, scripts and vars are unequal.\n")
    if len>0:
        for i in range(len-1,-1,-1):
            Director.eraseSaveString(plr, "mission_scripts", i)
            Director.eraseSaveString(plr, "mission_names", i)
            Director.eraseSaveString(plr, "mission_descriptions", i)
            Director.eraseSaveString(plr, "mission_vars", i)

use_missioncomputer=1
fixer_has_rescue=0
fixer_has_wingman=0
initial_fixerpct=0.02
initial_guildpct=0.4
fixerpct=initial_fixerpct
guildpct=initial_guildpct
def restoreFixerPct():
    global fixerpct
    global guildpct
    global initial_fixerpct
    global initial_guildpct
    fixerpct=initial_fixerpct
    guildpct=initial_guildpct
def mungeFixerPct():
    global fixerpct
    global guildpct
    fixerpct=.0375
    guildpct=1

def generateCleansweepMission(path,numplanets,enemy):
    fighterprob=vsrandom.random()*.75+.25;
    capshipprob=0.0
    if (vsrandom.random()<.06125):
        capshipprob=vsrandom.random()*.25;
    forceattack=vsrandom.randrange(0,2)
    cleansweep=1#vsrandom.randrange(0,2)
    minships=maxships=vsrandom.randrange(1,4)
    creds = 3*(cleansweep+1+capshipprob*2+.25*forceattack)*800*minships*fighterprob+1.2*syscreds*len(path)
    creds*=getPriceModifier(False)
    addstr=""
    isFixer=vsrandom.random()
    if isFixer<fixerpct:
        creds*=2
        addstr+="#F#bases/fixers/confed.spr#Talk to the Confed Officer#Thank you.  Your help makes space a safer place.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        if (cleansweep):
            addstr+="#G#Bounty#\n"
        else:
            addstr+="#G#Patrol#\n"
    elif use_missioncomputer:
        if (cleansweep):
            addstr+="#C#Bounty#\n"
        else:
            addstr+="#C#Patrol#\n"
    missiontype="patrol_enemies"
    additional=()
    additionalinstructions=""
    patrolorclean="Patrol"
    dist=1000
    if (cleansweep):
        dist=1500
        additional=(1,)
        patrolorclean="Clean_Sweep"
        missiontype="cleansweep"
        additionalinstructions+=""
    if (capshipprob):
        additionalinstructions+=" Capital ships possibly in the area."

    randCompany = GetRandomCompanyName()
    attackb = GetRandomAttackBrief()
    composedBrief = attackb.replace('$CL',randCompany)
    composedBrief = composedBrief.replace('$MT',enemy)
    composedBrief = composedBrief.replace('$NP',str(int(numplanets)))
    composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
    composedBrief = composedBrief.replace('$PY',str(int(creds)))
    composedBrief = composedBrief.replace('$IN',additionalinstructions)
    ispoint="s"
    if numplanets==1:
        ispoint=""
    if len(path)==1:
        mistype = 'IN-SYSTEM ATTACK'
    else:
        mistype = 'ATTACK'
    writedescription(composedBrief)
    writemissionsavegame (addstr+mission_script_template % dict(
        module=missiontype,
        constructor=missiontype,
        args=(0,numplanets,dist,creds,path,'',minships,maxships,fighterprob,capshipprob,enemy,forceattack)+additional))

    writemissionname("%s/%s_%d_Point%s_in_%s"%(patrolorclean,patrolorclean,numplanets,ispoint, processSystem(path[-1])),path,isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def generatePatrolMission (path,numplanets,enemy):
    print ("Generate Patrol Mission")
    dist=400
    minships=0
    fighterprob=vsrandom.random()*.75;
    capshipprob=vsrandom.random()*.01;
    forceattack=vsrandom.randrange(0,2)
    maxships=vsrandom.randrange(1,4)
    creds = numplanets*100+3*800+syscreds*len(path)
    creds = (capshipprob*4+.5*forceattack+fighterprob+1)*200*numplanets*maxships+.5*syscreds*len(path)
    additional=()
    additionalinstructions=""
    creds*=getPriceModifier(False)
    addstr=""
    isFixer=vsrandom.random()
    if isFixer<fixerpct:
        creds*=2
        addstr+="#F#bases/fixers/confed.spr#Talk to the Confed Officer#Thank you.  Your help makes space a safer place.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Patrol#\n"
    elif use_missioncomputer:
        addstr+="#C#Patrol#\n"
    randCompany = GetRandomCompanyName()
    patrolb = GetRandomPatrolBrief()
    composedBrief = patrolb.replace('$CL',randCompany)
    composedBrief = composedBrief.replace('$NP',str(int(numplanets)))
    composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
    composedBrief = composedBrief.replace('$PY',str(int(creds)))
    ispoint="s"
    if numplanets==1:
        ispoint=""
    if len(path)==1:
        mistype = 'IN-SYSTEM PATROL'
    else:
        mistype = 'PATROL'
    writedescription(composedBrief)
    writemissionsavegame (addstr+mission_script_template % dict(
        module='patrol_enemies',
        constructor='patrol_enemies',
        args=(0, numplanets, dist, creds, path, '', minships, maxships, fighterprob, capshipprob, enemy, forceattack) + additional))
    writemissionname("Patrol/Patrol_%d_Point%s_in_%s"%(numplanets,ispoint, processSystem(path[-1])),path,isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def isNotWorthy(fac):
    return VS.GetRelation(fac,VS.getPlayer().getFactionName())<0
def generateEscortLocal(path,fg,fac):
    if (isNotWorthy(fac)):
        return
    typ = fg_util.RandomShipIn(fg,fac)
    if typ in faction_ships.unescortable:
        typ = faction_ships.unescortable[typ]
    enfac = faction_ships.get_enemy_of(fac)
    diff=vsrandom.randrange(1,4)
    waves=vsrandom.randrange(0,5-diff)
    incoming=vsrandom.randrange(0,2)
    enfg =fg_util.AllFGsInSystem(enfac,path[-1])
    creds=1050.0*diff*(1+waves);
    if (len(enfg)):
      enfg=enfg[vsrandom.randrange(0,len(enfg))]
    else:
      enfg=''
    isFixer=vsrandom.random()
    addstr=""
    if isFixer<fixerpct:
        creds*=2
        addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust that you will safely guide my collegue until he reaches the destination.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Escort#\n"
    elif use_missioncomputer:
        addstr+="#C#Escort#\n"
    additionalinfo="to the jump point"
    if (incoming):
        additionalinfo="from the jump point to a nearby base"
    randCompany = GetRandomCompanyName()
    escortb = GetRandomEscortBrief()
    composedBrief = escortb.replace('$CL',randCompany)
    composedBrief = composedBrief.replace('$MT',enfac)
    composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
    composedBrief = composedBrief.replace('$PY',str(int(creds)))
    composedBrief = composedBrief.replace('$AI',additionalinfo)
    composedBrief = composedBrief.replace('$ET',formatShip(typ))
    if len(path)==1:
        mistype = 'IN-SYSTEM ESCORT'
    else:
        mistype = 'ESCORT'
    writedescription(composedBrief)
    writemissionsavegame(addstr+mission_script_template % dict(
        module='escort_local',
        constructor='escort_local',
        args=(enfac,0,diff,waves,500,creds,incoming,fac,(),'',enfg,'',fg,typ)))
    writemissionname("Escort/Escort_%s_%s"%(fac,fg),[path[-1]],isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def generateEscortMission (path,fg,fac):
    ###
    if (isNotWorthy(fac)):
        return
    typ = fg_util.RandomShipIn(fg,fac)
    if typ in faction_ships.unescortable:
        typ = faction_ships.unescortable[typ]
    diff=vsrandom.randrange(0,6)
    creds=250*diff+1.2*syscreds*len(path)
    creds*=getPriceModifier(False)
    addstr=""
    isFixer=vsrandom.random()
    if isFixer<fixerpct:
        creds*=2
        addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust that you will safely guide my collegue until you reach the destination.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Escort#\n"
    elif use_missioncomputer:
        addstr+="#C#Escort#\n"
    if len(path)==1:
        mistype = 'IN-SYSTEM ESCORT'
    else:
        mistype = 'ESCORT'
    writemissionsavegame (addstr+mission_script_template % dict(
        module='escort_mission',
        constructor='escort_mission',
        args=(fac,diff,float(creds),0,0,path,'',fg,typ)))
    writedescription("The %s %s in the %s flightgroup requres an escort to %s. The reward for a successful escort is %d credits."%(fac,formatShip(typ),fg, processSystem(path[-1]),creds))
    writemissionname("Escort/Escort_%s_%s_to_%s"%(fac,fg,processSystem(path[-1])),path,isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def changecat(category):
    l=category.split('/')
    if len(l)>1:
        return l[-1]+'_'+l[0]
    else:
        return category

def pathWarning(path,isFixer):
    global dnewsman_
    message = str()
    factions = list()
    if isFixer:
        message+="\nPrecautions taken to ensure the success of this mission should be taken at your expense."
    else:
        for system in path:
            sysfac = VS.GetGalaxyFaction(system)
            if sysfac not in factions:
                factions.append(sysfac)
        message+="\n\nYou are responsible for the success of this mission.  Precautions taken to ensure this outcome will be taken at your expense.  With that in mind, I will advise you that you will be travalling through systems dominated by the "
        if len(factions) == 1:
            message+=dnewsman_.data.getFactionData(factions[0],'full')[0]+"."
        else:
            message+="following factions: "
            jj=0
            for fac in factions:
                jj+=1               
                message+=dnewsman_.data.getFactionData(fac,'full')[0]
                if jj<len(factions)-1:
                    message+=", "
                elif jj<len(factions):
                    message+=" and "
    return message
def adjustQuantityDifficulty(max):
   return 3+int((max-3)*VS.GetDifficulty())
def isHabitable (system):
    planetlist=VS.GetGalaxyProperty(system,"planets")
    if (len(planetlist)==0):
        return False
    planets=planetlist.split(' ')
    for planet in planets:
        if planet=="i" or planet=="a" or planet=="am" or planet=="u" or planet=="com" or planet=="bd" or planet=="s" or planet=="o" or planet=="at" or planet=="bs" or planet=="bdm" or planet=="bsm" or planet=="f" or planet=="fm" or planet=="t":
            return True
    debug.debug(str(planets)+ " Not in Habitable List")
    return False
def generateCargoMission (path, numcargos,category, fac):
    #if (isNotWorthy(fac)):
    #    return
    if (vsrandom.random()<.25):
        return  
    launchcap=0
    if (not launchcap) and not isHabitable(path[-1]):
        return
    diff=vsrandom.randrange(0,adjustQuantityDifficulty(6))
    creds=65*numcargos+145*diff+syscreds*len(path)+3250*(category[:10]=="Contraband")+5000*(category[:9]=="starships")
    addstr=""
    creds*=getPriceModifier(False)
    isFixer=vsrandom.random()
    if isFixer<fixerpct:
        creds*=2
        addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust you will make the delivery successfully.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Cargo#\n"
    elif use_missioncomputer:
        addstr+="#C#Cargo#\n"
    writemissionsavegame (addstr+mission_script_template % dict(
        module='cargo_mission',
        constructor='cargo_mission',
        args=(fac,0,numcargos,diff,creds,launchcap,0,category,path,'')))
    if (category==''):
        category='generic'
    randCompany = GetRandomCompanyName()
    if (randCompany==''):
        strStart = "We need to deliver some "
    else:
    	  strStart = randCompany+" seeks delivery of "    	  
    if len(path)==1:
        mistype = 'IN-SYSTEM CARGO'
    else:
        mistype = 'CARGO'
    brief = GetRandomCargoBrief()
#    if (brief<>''):
    if (brief!=''):
        composedBrief = brief.replace('$CL',randCompany)
        composedBrief = composedBrief.replace('$CG',formatCargoCategory(category))
        composedBrief = composedBrief.replace(' $DB','')
        composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
        composedBrief = composedBrief.replace('$PY',str(int(creds)))
        writedescription(composedBrief)
    else:
        writedescription(strStart+"%s cargo to the %s system. The mission is worth %d credits to us.  You will deliver it to a base owned by the %s.%s"%(formatCargoCategory(category), processSystem(path[-1]),creds,fac,pathWarning(path,isFixer<guildpct)))
    writemissionname("Cargo/Deliver_%s_to_%s"%(changecat(category),processSystem(path[-1])),path,isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def generateRescueMission(path,rescuelist):
    makemissionharder=vsrandom.randrange(0,2)
    numships = vsrandom.randrange(1,adjustQuantityDifficulty(6))+howMuchHarder(makemissionharder)
    creds = (numships+len(path))*vsrandom.randrange(1041,1640)
    creds*=getPriceModifier(makemissionharder!=0)
    if (creds>20000):
        creds=21000
    randCompany = GetRandomCompanyName()
    rescueb = GetRandomRescueBrief()
    composedBrief = rescueb.replace('$CL',randCompany)
    composedBrief = composedBrief.replace('$MT',rescuelist[0])
    composedBrief = composedBrief.replace('$AT',str(int(numships)))
    composedBrief = composedBrief.replace('$AN',rescuelist[2])
    composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
    composedBrief = composedBrief.replace('$PY',str(int(creds)))
    addstr = ""
    isFixer=vsrandom.random()
    if isFixer<fixerpct and fixer_has_rescue:
        creds*=2
        addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust you will make the delivery successfully.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Rescue#\n"
    elif use_missioncomputer:
        addstr+="#C#Rescue#\n"
    if len(path)==1:
        mistype = 'IN-SYSTEM RESCUE'
    else:
        mistype = 'RESCUE'
    writedescription(composedBrief)
    writemissionsavegame (addstr+mission_script_template % dict(
        module='rescue',
        constructor='rescue',
        args=(creds,0,rescuelist[0],numships,rescuelist[2],rescuelist[1],path)))
    writemissionname("Rescue/Rescue_%s_from_%s_ships"%(rescuelist[0],rescuelist[2]),path,0)
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def generateBountyMission (path,fg,fac):
    typ = fg_util.RandomShipIn(fg,fac)
    cap = faction_ships.isCapital(typ)
    makemissionharder=vsrandom.randrange(0,2)
    diff=vsrandom.randrange(0,adjustQuantityDifficulty(7))+howMuchHarder(makemissionharder)
    runaway=(vsrandom.random()>=.75)
    creds=750+1000*runaway+450*diff+syscreds*len(path)
    if (cap):
        creds*=4

    finalprice=creds+syscreds*len(path)
    finalprice*=getPriceModifier(False)
    addstr=""
    isFixer=vsrandom.random()
    if isFixer<fixerpct:
        finalprice*=2
        addstr+="#F#bases/fixers/hunter.spr#Talk with the Bounty Hunter#We will pay you on mission completion.  And as far as anyone knows-- we never met."
        if (runaway):
            addstr += '#Also-- we have information that the target may be informed about your attack and may be ready to run. Be quick!'
        addstr+="#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Bounty#\n"
    elif use_missioncomputer:
        addstr+="#C#Bounty#\n"
    writemissionsavegame (addstr+mission_script_template % dict(
        module='bounty',
        constructor='bounty',
        args=(0,0,finalprice,runaway,diff,fac,path,'',fg,typ)))
    diffstr = ""
    if (diff>0):
        diffstr="  The ship in question is thought to have %d starships for protection."%diff
    randCompany = GetRandomCompanyName()
    bountyb = GetRandomBountyBrief()
    composedBrief = bountyb.replace('$CL',randCompany)
    composedBrief = composedBrief.replace('$MT',formatShip(typ))
    composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
    composedBrief = composedBrief.replace('$PY',str(int(finalprice)))
    if len(path)==1:
        mistype = 'IN-SYSTEM BOUNTY'
    else:
        mistype = 'BOUNTY'
    writedescription(composedBrief)
    if (cap):
        writemissionname ("Bounty/on_%s_Capital_Vessel_in_%s"%(fac,processSystem(path[-1])),path,isFixerString(addstr))
    else:
        writemissionname ("Bounty/on_%s_starship_in_%s"%(fac,processSystem(path[-1])),path,isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )

def generateDefendMission (path,defendfg,defendfac, attackfg,attackfac):
    if (isNotWorthy(defendfac)):
        return
    #defendtyp = fg_util.RandomShipIn(defendfg,defendfac)
    attacktyp = fg_util.RandomShipIn(attackfg,attackfac)                    
    isbase=fg_util.BaseFGInSystemName(path[-1])==defendfg
    creds=1200
    minq = 1
    maxq = adjustQuantityDifficulty(5)
    makemissionharder=vsrandom.randrange(0,2)
    quantity = vsrandom.randrange(minq,maxq)+howMuchHarder(makemissionharder)
    reallydefend = "1"
    if (vsrandom.randrange(0,4)==0):
        reallydefend="0"
    addstr=""
    creds=creds*quantity+syscreds*len(path)
    creds*=getPriceModifier(makemissionharder)
    isFixer=vsrandom.random()
    if isFixer<fixerpct:
        creds*=2
        addstr+="#F#bases/fixers/confed.spr#Talk to the Confed Officer#Thank you. Your defense will help confed in the long run.  We appreciate the support of the bounty hunting community.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Defend#\n"
    elif use_missioncomputer:
        addstr+="#C#Defend#\n"
    writemissionsavegame (addstr+mission_script_template % dict(
        module='defend',
        constructor='defend',
        args=(attackfac,0,quantity,8000.0,100000.0,creds,reallydefend,isbase,defendfac,path,'',attackfg,attacktyp,defendfg)))
    iscapitol=""
    if isbase:
        iscapitol="capital "
    randCompany = GetRandomCompanyName()
    defendb = GetRandomDefendBrief()
    composedBrief = defendb.replace('$CL',randCompany)
    composedBrief = composedBrief.replace('$DT',iscapitol)
    composedBrief = composedBrief.replace('$DS',processSystem(path[-1]))
    composedBrief = composedBrief.replace('$PY',str(int(creds)))
    composedBrief = composedBrief.replace('$MT',attackfac)
    if len(path)==1:
        mistype = 'IN-SYSTEM DEFEND'
    else:
        mistype = 'DEFEND'
    writedescription(composedBrief)
    writemissionname("Defend/Defend_%s_from_%s"%(defendfac, attackfac),path,isFixerString(addstr))
    writemissionvars( { 'MISSION_TYPE' : mistype } )


def generateWingmanMission(fg, faction):
    numships=vsrandom.randrange(1,4)
    creds=10000+15000*numships
    writemissionsavegame ('#\n' + mission_script_template % dict(
        module='wingman',
        constructor='wingman',
        args=(creds,faction,numships,0)))
    s="A pilot"
    EorA="a"
    are="is"
    if numships > 1:
        s=str(numships)+" pilots"
        EorA="e"
        are="are"
    isFixer=vsrandom.random()
    if isFixer<fixerpct and fixer_has_wingman:
        creds*=2
        addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust you will make the delivery successfully.#\n"
    elif isFixer<guildpct:
        creds*=1.5
        addstr+="#G#Wingman#\n"
    elif use_missioncomputer:
        addstr+="#C#Wingman#\n"
    writedescription(s+" in the %s faction %s willing to help you out and fight with you as long as you pay %d credits."%(faction, are, creds))
    writemissionname("Wingmen/Hire_%d_%s_Wingm%sn"%(numships,faction,EorA),[VS.getSystemFile()],0)
    writemissionvars( { 'MISSION_TYPE' : 'CONTRACT WINGMAN' } )
    
    
def GetFactionToDefend(thisfaction, fac, cursys):
    m = fg_util.FGsInSystem ("merchant",cursys)
    nummerchant=len(m)
    m+=fg_util.FGsInSystem (thisfaction,cursys)
    numthisfac=len(m)
    m+=fg_util.FGsInSystem (fac,cursys)
    return (m,nummerchant,numthisfac)

def contractMissionsFor(fac,baseship,minsysaway,maxsysaway):
    global totalMissionNumber
    global insysMissionNumber
    totalMissionNumber=0
    insysMissionNumber=0
    facnum=faction_ships.factionToInt(fac)
    enemies = list(faction_ships.enemies[facnum])
    script=''
    cursystem = VS.getSystemFile()
    thisfaction = VS.GetGalaxyFaction (cursystem)
    preferredfaction=None
    if (VS.GetRelation (fac,thisfaction)>=0):
        preferredfaction=thisfaction#try to stay in this territory
    l=[]
    num_wingmen=2
    num_rescue=2
    num_defend=1
    num_idefend=2
    num_bounty=1
    num_ibounty=1
    num_patrol=1
    num_ipatrol=1
    num_escort=1
    num_iescort=1
    mincount=2
    usedcats={}
    for i in range (minsysaway,maxsysaway+1):
        for j in getSystemsNAway(cursystem,i,preferredfaction):
            import dynamic_battle
            if (i<2 and num_rescue>0):
                if j[-1] in dynamic_battle.rescuelist:
                    generateRescueMission(j,dynamic_battle.rescuelist[j[-1]])
                    if checkCreatedMission():
                        num_rescue-=1
#            if (0 and i==0):
#                generateRescueMission(j,("confed","Shadow","pirates"))
            l = dynamic_battle.BattlesInSystem(j[-1])
            nodefend=1
            for k in l:
                if (VS.GetRelation(fac,k[1][1])>=0):
                    if ((j[-1]==VS.getSystemFile() and num_idefend<=0) or (j[-1]!=VS.getSystemFile() and num_defend<=0)):
                        mungeFixerPct()
                        print ("Munged")
                    else:
                        nodefend=0
                    generateDefendMission(j,k[1][0],k[1][1],k[0][0],k[0][1])
                    restoreFixerPct()
                    if checkInsysNum():
                        num_idefend-=1
                    if checkMissionNum():
                        num_defend-=1
                    print ("Generated defendX with insys at: "+str(num_idefend)+" and outsys at "+str (num_defend))
            (m,nummerchant,numthisfac)=GetFactionToDefend(thisfaction, fac, j[-1])

            if preferredfaction:
                for kk in faction_ships.enemies[faction_ships.factiondict[thisfaction]]:
                    k=faction_ships.intToFaction(kk)
                    for mm in fg_util.FGsInSystem(k,j[-1]):
                        if (i==0 or vsrandom.randrange(0,4)==0):#fixme betterthan 4
                            if nodefend and len(m) and vsrandom.random()<.4:
                                if 1:#for i in range(vsrandom.randrange(1,3)):
                                    insys=(j[-1]==VS.getSystemFile())
                                    if (insys and num_idefend<=0):
                                        mungeFixerPct()
                                    elif (num_defend<=0 and not insys):
                                        mungeFixerPct()
                                    rnd=vsrandom.randrange(0,len(m))
                                    def_fg=m[rnd]
                                    def_fac = "merchant"
                                    if rnd>=nummerchant:
                                        def_fac= thisfaction
                                    if rnd>=numthisfac:
                                        def_fac = fac
                                    generateDefendMission(j,def_fg,def_fac,mm,k)
                                    restoreFixerPct()
                                    if checkInsysNum():
                                        num_idefend-=1
                                    if checkMissionNum():
                                        num_defend-=1
                                    print ("Generated defendY with insys at: "+str(num_idefend)+" and outsys at "+str (num_defend))
                                nodefend=0
                            elif ((i==0 or vsrandom.random()<.5)):
                                if ((j[-1]==VS.getSystemFile() and num_ibounty<=0) or (j[-1]!=VS.getSystemFile() and num_bounty<=0)):
                                   mungeFixerPct()
                                generateBountyMission(j,mm,k)
                                restoreFixerPct()
                                if checkInsysNum():
                                    print (" decrementing INSYS bounty to "+str(num_ibounty))
                                    num_ibounty-=1
                                if checkMissionNum():
                                    print (" decrementing bounty to "+str(num_bounty))
                                    num_bounty-=1



            mincount=-2
            if i==0:
                mincount=1
            for k in range(vsrandom.randrange(mincount,8)): ###FIXME: choose a better number than 4.
                if k<0:
                    k=0
                rnd=vsrandom.random()
                if (rnd<.15):    # 15% - nothing
                    pass
                if (rnd<.5 or i==0):    # 35% - Patrol Mission
                    if ((j[-1]==VS.getSystemFile() and num_ipatrol<=0) or (j[-1]!=VS.getSystemFile() and num_patrol<=0)):
                        mungeFixerPct()
                    if (vsrandom.randrange(0,2) or j[-1] in faction_ships.fortress_systems):
                        generatePatrolMission(j,numPatrolPoints(j[-1]),faction_ships.get_enemy_of(fac))
                    else:
                        generateCleansweepMission(j,numPatrolPoints(j[-1]),faction_ships.get_enemy_of(fac))
                    restoreFixerPct()
                    if checkInsysNum():
                        num_ipatrol-=1
                    if checkMissionNum():
                        num_patrol-=1
                        
                else:   # 50% - Cargo mission
                    numcargos=vsrandom.randrange(1,25)

                    playership=VS.getPlayer().getName()
                    try:
                        hold=int(VS.LookupUnitStat(playership,"privateer","Hold_Volume"))
                    except:
                        hold=10;
                    if hold==0:
                        hold=10;
                    numcargos=10
                    #ignore hold contents

                    category=''
                    if (rnd>.87 and fac!='confed' and fac != "ISO" and fac!="militia" and fac!="homeland-security" and fac!="kilrathi" and fac!="merchant"):
                        category='Contraband'
                    else:
                        for myiter in range (100):
                            carg=VS.getRandCargo(numcargos,category)
                            category=carg.GetCategory()
                            if (category[:9] != 'Fragments' and category[:10]!='Contraband' and category.find('upgrades')!=0 and (category.find('starships')!=0 or rnd>.999)):
                                break 
                            if (myiter!=99):
                                category=''
                        if baseship:
                            faction=fac
                            name=baseship.getName()
                            if baseship.isPlanet():
                                faction="planets"
                                name=baseship.getFullname()
                            print ("TRADING")
                            import trading
                            print (name)
                            print (faction)
                            exports=trading.getNoStarshipExports(name,faction,20)
                            print (exports)
                            if (category.find("assengers")==-1 and len(exports)):
                                category=exports[vsrandom.randrange(0,len(exports))][0]

#                    print ("CATEGORY OK "+category)
                    if not category in usedcats or category[:10]=='Contraband':
                        generateCargoMission(j,numcargos,category,fac)
                        usedcats[category]=1
                numescort = vsrandom.randrange(0,2)
                if (numescort>len(m)):
                    numescort=len(m)
                count=0
                for k in m:
                    if (i==0):
                        if vsrandom.random()<.92:
                            count+=1
                            continue
                    elif (vsrandom.random()<.97):
                        count+=1
                        continue
                    f = "merchant"
                    if count>=nummerchant:
                        f= thisfaction
                    if count>=numthisfac:
                        f = fac
                    if (vsrandom.random()<.25):
                        if (num_wingmen>0):
                            #generateWingmanMission(k,f)
                            num_wingmen-=1
                    elif (i==0):
                        if (vsrandom.random()<.25):
                            if num_iescort<=0:
                                mungeFixerPct()
                            #generateEscortLocal(j,k,f)
                            restoreFixerPct()
                            if checkCreatedMission():                    
                                num_iescort-=1
                    else:
                        if num_escort<=0:
                            mungeFixerPct()
                        generateEscortLocal(j,k,f)
                        restoreFixerPct()
                        if checkCreatedMission():                    
                            num_escort-=1

                    count+=1

def CreateMissions(minsys=0,maxsys=4):
    generate_dyn_universe.KeepUniverseGenerated()
    if VS.networked():
        # No generating stuff while networked.
        return
    eraseExtras()
    i=0
    global plr,basefac,baseship
    plrun=VS.getPlayer()
    plr=plrun.isPlayerStarship()
    i = VS.getUnitList()
    while(not i.isDone() and not i.current().isDocked(plrun)):
        i.advance()
    if (not i.isDone()):
        basefac=i.current().getFactionName()
    if (basefac=='neutral'):
        basefac=VS.GetGalaxyFaction(VS.getSystemFile())
    contractMissionsFor(basefac,baseship,minsys,maxsys)
    import news
    news.processNews(plr)
    print ("GOOG GOOO")
