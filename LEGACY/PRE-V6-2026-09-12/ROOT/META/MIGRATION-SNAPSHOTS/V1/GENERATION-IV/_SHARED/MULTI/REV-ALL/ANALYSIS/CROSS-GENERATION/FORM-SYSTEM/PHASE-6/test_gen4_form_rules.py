ROTOM = {0:None,1:"OVERHEAT",2:"HYDRO_PUMP",3:"BLIZZARD",4:"AIR_SLASH",5:"LEAF_STORM"}
THUNDER_SHOCK="THUNDER_SHOCK"

def set_rotom_form(moves, form, fallback_slot=0):
    moves=list(moves); new=ROTOM[form]; appliance=set(x for x in ROTOM.values() if x)
    i=0
    while i<4:
        if moves[i] in appliance:
            if new is not None:
                moves[i]=new; new=None
            else:
                moves.pop(i); moves.append(None); continue
        i+=1
    if new is not None:
        try: moves[moves.index(None)] = new
        except ValueError: moves[fallback_slot]=new
    if moves[0] is None: moves[0]=THUNDER_SHOCK
    return moves

def shaymin_can_gracidea(species,form,hp,fateful,frozen,hour):
    return species==492 and form==0 and hp>0 and fateful and not frozen and 4<=hour<20

def giratina_form(item_is_orb,distortion_world=False):
    return 1 if item_is_orb or distortion_world else 0

ARCEUS={"NONE":0,"FIGHTING":1,"FLYING":2,"POISON":3,"GROUND":4,"ROCK":5,"BUG":6,"GHOST":7,"STEEL":8,"FIRE":10,"WATER":11,"GRASS":12,"ELECTRIC":13,"PSYCHIC":14,"ICE":15,"DRAGON":16,"DARK":17}

assert set_rotom_form(["TACKLE","OVERHEAT","SHOCK_WAVE",None],2)==["TACKLE","HYDRO_PUMP","SHOCK_WAVE",None]
assert set_rotom_form(["OVERHEAT","TACKLE",None,None],0)==["TACKLE",None,None,None]
assert set_rotom_form(["OVERHEAT",None,None,None],0)[0]==THUNDER_SHOCK
assert set_rotom_form(["A","B","C","D"],5,2)==["A","B","LEAF_STORM","D"]
assert not shaymin_can_gracidea(492,0,100,True,False,3)
assert shaymin_can_gracidea(492,0,100,True,False,4)
assert shaymin_can_gracidea(492,0,100,True,False,19)
assert not shaymin_can_gracidea(492,0,100,True,False,20)
assert not shaymin_can_gracidea(492,0,100,True,True,12)
assert not shaymin_can_gracidea(492,0,0,True,False,12)
assert not shaymin_can_gracidea(492,0,100,False,False,12)
assert not shaymin_can_gracidea(492,1,100,True,False,12)
assert giratina_form(False,False)==0
assert giratina_form(True,False)==1
assert giratina_form(False,True)==1
assert set(ARCEUS.values())==set(range(18))-{9}
assert ARCEUS["FIRE"]==10 and ARCEUS["DARK"]==17
print("Phase 6 form-rule proof: PASS")
