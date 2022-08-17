import GUI
import Base
import VS
import methodtype
import universe

from XGUIDebug import trace
_trace_level = 3
PURCHASE_MAX = 10

def MakeCommodity(room_from,time_of_day='_day'):
    # create the commodity exchange
    room_id = Base.Room ('Commodity_Exchange')
    comp = CommodityComputer(room_id)

    Base.Link (room_id, 'exit', -1, -1, 2, 0.2513, 'Exit', room_from)
    return room_id

def MakeCommodityLink(room_from, x, y, w, h, label=None):
    if label == None:
        label = 'Commodity_Exchange'

    room_commodity = MakeCommodity(room_from)

    # create an interstitial screen
    room_start = Base.Room ('XXXCommodity_Exchange_Loading')
    animation = CommodityComputerAnimation(room_start, room_commodity)

    # add the link which calls Python code, restarting the animation
    #Base.Link (room_commodity, 'commodities', x, y, w, h, label, room_from)
    Base.LinkPython (room_from, 'commodities', """#
import GUI
GUI.GUIRootSingleton.rooms[%s].owner.reset()
""" %(room_start), x, y, w, h, label, room_start)


class CommodityComputerAnimation:
    def __init__(self,room_start,room_next):
        # create GUIRoom object
        guiroom  = GUI.GUIRoom(room_start)
        self.guiroom = guiroom
        self.room_next  = room_next

        # let us find this object via GUIRootSingleton.rooms[x].owner or GUIElement.room.owner
        guiroom.owner = self

        # draw the background image
        GUI.GUIStaticImage(guiroom, 'background', ( 'interfaces/commodity/Commodity.spr', GUI.GUINPOTRect(0, 0, 320, 200, 320, 200, "pixel") ))
        self.computer   = GUI.GUIStaticImage(guiroom, 'animation', ( 'interfaces/commodity/ani.spr', GUI.GUIRect(0, 0, 132, 100, "pixel") ))

        # draw now
        GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index, 'draw', None)

        # undraw the animation, so that when reset is called, it runs from the beginning
        # NOTE: using hide() here doesn't work, as of the current version of GUI.py
        self.computer.undraw()
        
    def reset(self):
        room_start = self.guiroom.getIndex()
        room_next  = self.room_next
        self.computer.draw()

        # reset the commodity exchange computer
        GUI.GUIRootSingleton.rooms[room_next].owner.reset()

        # add script which will automatically switch from intro to main page
        Base.RunScript(room_start, "redirect", """#
import Base
Base.SetCurRoom(%s)
Base.EraseObj(%s,"redirect")
import GUI
GUI.GUIRootSingleton.rooms[%s].owner.computer.undraw()
""" %(room_next, room_start, room_start), 2.0)
    
def mode_click(self,params):
    GUI.GUIRadioButton.onClick(self,params)
    if self.isEnabled():
        self.room.owner.set_state(self.index)

def next_click(self,params):
    GUI.GUIButton.onClick(self,params)
#    self.room.owner.next()
    next(self.room.owner)

def prev_click(self,params):
    GUI.GUIButton.onClick(self,params)
    self.room.owner.previous()

def select_click(self,params):
    GUI.GUIButton.onClick(self,params)
    # temp until shift-click (or ctrl-click, or alt-click) gets fixed
#    print "::: CommodityComputer select_click params = "
    print ("::: CommodityComputer select_click params = ")
    import pprint
    pprint.pprint(params)
    if ('shift' in params):
        self.room.owner.select(params['shift'])
    else:
        self.room.owner.select()


# see http://docs.python.org/ref/customization.html for info on __init__, __str__, etc
class CommodityComputer:
    """
        This class basically handles 5 things:
        1) a list of prices for all commodities
        2) a list of the commodities available to buy (type and count)
        3) a list of the commodities the user owns (type and count)
        4) the actual workings of the commodity computer; buy/sell mode, current item
        5) buttons, text, images needed to accomplish #4
    """
    
    def __init__(self,room_id):
        self.room_id  = room_id

        # initial state is "buy"
        self.state = "buy"
        self.current_item = 0

        # add GUI to commodity computer
        guiroom  = GUI.GUIRoom(room_id)
        self.guiroom = guiroom


        # when a button is clicked, this will allow us to get the CommodityComputer instance from the x_click functions
        guiroom.owner = self

        # draw the background images
        background = GUI.GUIStaticImage(guiroom, 'background', ( 'interfaces/commodity/Commodity.spr', GUI.GUINPOTRect(0, 0, 320, 200, 320, 200, "pixel") ))
#        computer   = GUI.GUIStaticImage(guiroom, 'computer', ( 'interfaces/commodity/Commodity_Computer.spr', GUI.GUINPOTRect(0, 0, 320, 200, 320, 200, "pixel") ))
        computer   = GUI.GUIStaticImage(guiroom, 'computer', ( 'interfaces/commodity/Commodity_Computer_hi.spr', GUI.GUIRect(0, 0, 132, 100, "pixel") ))

        self.buttons = {}

#        buy_sprite  = ('interfaces/commodity/buy.spr',  GUI.GUINPOTRect(0, 0, 320, 200, 320, 200))
#        sell_sprite = ('interfaces/commodity/sell.spr', GUI.GUINPOTRect(0, 0, 320, 200, 320, 200))
        # pixel coordinates fractional because art is 1024x1024 and screen is at 320x200
        buy_sprite  = ('interfaces/commodity/buy_hi.spr' , GUI.GUIRect(71.5625, 79.4921875, 25.3125, 8.984375))
        sell_sprite = ('interfaces/commodity/sell_hi.spr', GUI.GUIRect(26.8750, 79.4921875, 25.3125, 9.1796875)) 
        buy_sprset  = { 'checked': buy_sprite, 'unchecked': None, 'hot': buy_sprite }
        sell_sprset = { 'checked': sell_sprite, 'unchecked': None, 'hot': sell_sprite }
        prev_sprset = {'enabled':None, 'disabled':None }
        next_sprset = {'disabled':None }
        self.add_button( GUI.GUIButton     (guiroom, 'Next Item',          'btn_next',   next_sprset, GUI.GUIRect(122, 26, 7, 14)                  ), next_click )
        self.add_button( GUI.GUIButton     (guiroom, 'Previous Item',      'btn_prev',   prev_sprset, GUI.GUIRect(122, 44, 7, 14)                  ), prev_click )
        self.add_button( GUI.GUIRadioButton(guiroom, 'Activate Buy Mode',  'btn_buy',    buy_sprset,  GUI.GUIRect( 72, 80, 25, 9), 'commodity_mode'), mode_click )
        self.add_button( GUI.GUIRadioButton(guiroom, 'Activate Sell Mode', 'btn_sell',   sell_sprset, GUI.GUIRect( 27, 80, 25, 9), 'commodity_mode'), mode_click )
        self.add_button( GUI.GUIButton     (guiroom, 'Select Items',       'btn_select', {},          GUI.GUIRect(13, 13, 97, 60)                  ), select_click )

        # set the check button state
        if (self.state == "buy"):
            GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index,'check',{'index':'btn_buy'})
        elif (self.state == "sell"):
            GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index,'check',{'index':'btn_sell'})
    
        # add the text labels
        txt_color = GUI.GUIColor(0.7,0.7,0.7)
        txt_warning_color = GUI.GUIColor(0.7,0,0)
        self.txt_name     = GUI.GUIStaticText(guiroom,'txt_name',    '', GUI.GUIRect(15, 12, 98, 10), txt_color)
        self.txt_quantity = GUI.GUIStaticText(guiroom,'txt_quantity','', GUI.GUIRect(15, 17, 98, 10), txt_color)
        self.txt_cost     = GUI.GUIStaticText(guiroom,'txt_cost',    '', GUI.GUIRect(15, 62, 98, 10), txt_color)
        self.txt_credits  = GUI.GUIStaticText(guiroom,'txt_credits', '', GUI.GUIRect(15, 67, 98, 10), txt_color)

        # add the item sprite (a blank sprite for now)
        self.img_item_rect = GUI.GUIRect(15, 9, 90, 67)
        self.img_item  = GUI.GUIStaticImage(guiroom, 'img_item', None)

        # error messages should appear above item images
        # something wrong with z-ordering here, so img_item will appear above txt_message
        # instead, set the y coord lower, so the text is readable
#        self.txt_message  = GUI.GUIStaticText(guiroom,'txt_message', '', GUI.GUIRect(15, 43, 98, 10), txt_color)
        self.txt_message  = GUI.GUIStaticText(guiroom,'txt_message', '', GUI.GUIRect(15, 57, 98, 10), txt_warning_color)

        # get the currently docked planet/space station
        current_base = universe.getDockedBase()

        # generate the global price list
        # if item doesn't appear on this list, it can't be bought or sold
        self.prices, self.exports = get_commodity_lists(current_base)
        self.imports, self.import_not_for_sale = get_player_manifest(self.prices)
        # sprites for cargo items
        self.sprites = get_sprite_info()

        # draw now
        GUI.GUIRootSingleton.broadcastRoomMessage(guiroom.index, 'draw', None)

        self.reset()

    def add_button(self, guibutton, onclick_handler):
        # add the button to the "buttons" dictionary, and add onclick handler
        self.buttons[guibutton.index] = guibutton
        guibutton.onClick = methodtype.methodtype(onclick_handler, guibutton, type(guibutton))

    def reset(self):
        # initial state is "buy"
        self.state = "buy"
        self.current_item = 0
        GUI.GUIRootSingleton.broadcastRoomMessage(self.guiroom.index,'check',{'index':'btn_buy'})
        
        # calculate cargo hold volume, and number of items for sale
        self.update_player_manifest()

        # draw the current_item in buy mode on the computer screen
        self.draw()
        self.guiroom.redrawIfNeeded()

    def draw(self,message=None):
        
        if self.state == "buy":
            if len(self.exports) > 0:
                # get the current item from the export list
                name, quant = self.exports[self.current_item]
                # get price
                try:
                    price = self.prices[name]
                except:
                    price = 10
                # get sprite
                try:
                    sprite = self.sprites[name]
                except:
                    sprite = 'interfaces/commodity/cargo/default.spr'

                self.drawItem(sprite,get_display_name(name),quant,price,VS.getPlayer().getCredits(),message)
            else:
                self.drawBlank("NOTHING TO BUY")

        elif self.state == "sell":
            # if len(player's cargo manifest) > 0  drawItem(current)
            # else
            if len(self.imports) > 0:
                # get the current item from the export list
                name, quant = self.imports[self.current_item]
                # get price
                try:
                    price = self.prices[name]
                except:
                    price = 10
                # get sprite
                try:
                    sprite = self.sprites[name]
                except:
                    sprite = 'interfaces/commodity/cargo/default.spr'
                self.drawItem(sprite,get_display_name(name),quant,price,VS.getPlayer().getCredits(),message)
            else:
                self.drawBlank("NOTHING TO SELL")

        else:
            self.drawBlank("Unknown state")

    def drawItem(self, spr_file, name, quantity, cost, credits, message=None):
        self.txt_name.setText( name )
        self.txt_quantity.setText( "Quantity: %s" %(quantity) )
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
            # calling self.txt_message.redraw() doesn't work to put txt_message above img_item

    def drawBlank(self,message=None):
        self.txt_name.setText('')
        self.txt_quantity.setText('')
        self.txt_cost.setText('')
        self.txt_credits.setText('')

        self.img_item.hide()

        if message==None:
            self.txt_message.setText('')
        else:
            self.txt_message.setText(message)

#    def next(self):
    def __next__(self):
        max = 0
        if self.state=="buy":
            max = len(self.exports)
        elif self.state=="sell":
            max = len(self.imports)
        if max > 0:
            self.current_item = (self.current_item + 1) % max
        else:
            self.current_item = 0
        self.draw()

    def previous(self):
        max = 0
        if self.state=="buy":
            max = len(self.exports) - 1
        elif self.state=="sell":
            max = len(self.imports) - 1
        self.current_item = self.current_item - 1
        if (self.current_item < 0):
            self.current_item = max
        self.draw()

    def update_player_manifest(self):
        # determine how much cargo capacity player has
        # this needs to be modified by cargo expansions & secret stash
        player = VS.getPlayer()
        self.player_hold_volume = int( VS.LookupUnitStat( player.getName(), player.getFactionName(), "Hold_Volume" ) )
        # capacity increases by 25 per cargo expansion
        # NOTE: this is NOT like original game; that increased size by 50% if they have the cargo expansion
        numaddcargo=player.hasCargo("add_cargo_expansion")
        if (numaddcargo):
            self.player_hold_volume = self.player_hold_volume + 25*numaddcargo
        numaddcargo=player.hasCargo("add_cargo_volume")
        if (numaddcargo):
            self.player_hold_volume = self.player_hold_volume + 50*numaddcargo
        numaddcargo=player.hasCargo("add_cargo_volume_galaxy")
        if (numaddcargo):
            self.player_hold_volume = self.player_hold_volume + 75*numaddcargo

        self.import_count = self.import_not_for_sale
#        for i in (range(len(self.imports))):
        for i in (list(range(len(self.imports)))):
            self.import_count = self.import_count + self.imports[i][1]
        trace(_trace_level, "::: update_player_manifest - hold volume = %s" %(self.player_hold_volume))
        trace(_trace_level, "::: update_player_manifest - hold contents = %s" %(self.import_count))

    def select(self,select_all=False):
        if self.state == "buy":
            # if player has sufficient cargo space and credits:
            # remove x items from exports
            # add x items to imports/player manifest
            # remove credits from players account
            if self.current_item < len(self.exports):
                # we have to call this, in case player has bought or sold ship or cargo expansion
                self.update_player_manifest()
                try:
                    player = VS.getPlayer()
                    current_base = universe.getDockedBase()
                    category = self.exports[self.current_item][0]
                    quantity = self.exports[self.current_item][1]
                    price = self.prices[category]
                    if (self.import_count >= self.player_hold_volume):
                        # if hold is full, display "NO ROOM"
                        self.draw("NO ROOM ON SHIP")

                    elif (price > VS.getPlayer().getCredits()):
                        # if player doesn't have enough credits, display "YOU'RE BROKE"
                        self.draw("INSUFFICIENT CREDITS")

                    else:
                        # otherwise, player has room and credits for at least 1 item
                        if (quantity > 0):
                            # commodity exchange has items to sell - item shouldn't be displayed if quantity is 0 anyway
                            
                            # calculate maximum player is able to buy; that is limited by:
                            #         quantity for sale
                            #        player's available storage
                            #        player's available credits
                            if price > 0:
                                count = min(
                                    quantity,
                                    (self.player_hold_volume - self.import_count),
                                    int(player.getCredits() / price) )
                            else:
                                # price should never be <= 0; just in case, avoid divide-by-zero or a negative count
                                trace(_trace_level, "::: commodity buy - price <= 0 : %s, %s" %(category, price))
                                count = min(
                                    quantity,
                                    (self.player_hold_volume - self.import_count) )

                            #
                            # transfer cargo from exchange to players ship
                            #
                            if not select_all:
                                # select_all == false means buying 1 at a time
                                if (count > 1):
                                    count=1
                            elif count > PURCHASE_MAX:
                                count = PURCHASE_MAX
                            transfer_count = transfer_cargo(current_base, player, category, price, count, self.player_hold_volume, self.import_count)

                            # update the commodity exchange exports list
                            self.exports[self.current_item][1] = quantity - transfer_count

                            # update the players imports list and
                            # increment the import_count value
                            self.import_count = self.import_count + transfer_count
                            import_index = -1
                            for i in range(len(self.imports)):
                                if self.imports[i][0] == category:
                                    import_index = i
                            if import_index == -1:
                                self.imports.append([category,transfer_count])
                            else:
                                self.imports[import_index][1] = self.imports[import_index][1] + transfer_count

                            # remove credits from players account
                            player.addCredits(-1 * transfer_count * price)
                            
                            # remove sprite from exports list if necessary
                            quantity = self.exports[self.current_item][1]
                            if quantity <= 0:
                                self.exports.pop(self.current_item)
                                if self.current_item >= len(self.exports):
                                    self.current_item = 0
                        else:
                            # quantity should never be <= 0
                            trace(_trace_level, "::: commodity buy - quantity <= 0 : %s, %s" %(category, quantity))
                        self.draw()
                except:
                    pass
        elif self.state == "sell":
            # remove x items from imports
            # add x items to exports
            # add credits to players account
            if self.current_item < len(self.imports):
                try:
                    player = VS.getPlayer()
                    current_base = universe.getDockedBase()
                    category = self.imports[self.current_item][0]
                    quantity = self.imports[self.current_item][1]
                    price = self.prices[category]
                    if (select_all):
                        count = quantity
                        if count > PURCHASE_MAX:
                            count = PURCHASE_MAX
                    else:
                        count = 1
                        
                    if ((quantity > 0) and (count <= quantity)):

                        #
                        # transfer cargo from players ship to exchange
                        #
                        transfer_count = transfer_cargo(player, current_base, category, price, count)

                        # update the players imports list
                        self.imports[self.current_item][1] = quantity - transfer_count
    
                        # update the commodity exchanges exports list
                        export_index = -1
                        for i in range(len(self.exports)):
                            if self.exports[i][0] == category:
                                export_index = i
                        if export_index == -1:
                            self.exports.append([category,transfer_count])
                        else:
                            self.exports[export_index][1] = self.exports[export_index][1] + transfer_count
    
                        # add credits to players account
                        player.addCredits(transfer_count * price)
    
                        # clean up if necessary
                        quantity = self.imports[self.current_item][1]
                        if quantity <= 0:
                            self.imports.pop(self.current_item)
                            if self.current_item >= len(self.imports):
                                self.current_item = 0

                except:
                    pass
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
        
    
"""
    returns the price list for the present base_type/faction
"""
def get_commodity_lists(current_base):
    trace(_trace_level, "::: DEBUG get_commodity_lists(%s) :::" %(current_base))
    # return values
    prices = {}
    exports = []

    if (0):
        # no longer done this way
        base_type = ''
        faction = ''

        import vsrandom
        import trading

        # local variables
        variability = {}    # price fluctuations
    
        # getImports etc return a list of 5 items:
        #    category
        #    price scale (i.e. 1.0 normal price, 1.3 30% increase
        #    price std deviation
        #    quantity
        #    quantity std deviation
        local_list  = trading.getImports(base_type, faction)
        master_list = VS.GetMasterPartList()
        
        for i in range(len(local_list)):
            cargo = local_list[i]
            category = cargo[0]
            if category[:8] == 'upgrades': continue
            if category[:9] == 'starships': continue
            variability[category] = cargo[1:3]
            quantity = int( vsrandom.gauss(cargo[3], cargo[4]) )
            if quantity > 0:
                # if there is a quantity available, add it to the export list
                exports.append([category, quantity])
        
        for i in range(master_list.numCargo()):
            cargo = master_list.GetCargoIndex(i)
            category = cargo.GetCategory()
        
            # move along if this item isn't a commodity
            if category == '': continue
            if category[:8] == 'upgrades': continue
            if category[:9] == 'starships': continue
        
            # get the price for this commodity
            baseprice = cargo.GetPrice()
            try:
                tmp = variability[category]
                variation = vsrandom.gauss(tmp[0], tmp[1])
                if (variation > 0.2):
                    # don't use very low or negative variations 
                    price = int( baseprice * variation )
                else:
                    price = int( baseprice )
            except:
                price = int( baseprice )
            prices[category] = price
    # end of old code

    for i in range(current_base.numCargo()):
        cargo = current_base.GetCargoIndex(i)

        name     = cargo.GetContent()
        category = cargo.GetCategory()
        quantity = cargo.GetQuantity()

        if name == '': continue
        if category[:8] == 'upgrades': continue
        if category[:9] == 'starships': continue
        
        try:
            price  = int( cargo.GetPrice() )
        except:
            price  = -1

        # at this point, if it isn't handled already by current_base, 
        # the price of contraband items on certain bases should be set to -1

        if (price > 0):
            prices[name] = price
            
        if (quantity > 0):
            exports.append([name, quantity])
            
            
    trace(_trace_level, "::: exports (%s %s %s)" %(current_base.getName(), current_base.getFullname(), current_base.getFactionName()))
    trace(_trace_level, repr( exports ))
    trace(_trace_level, "::: prices (%s %s %s)" %(current_base.getName(), current_base.getFullname(), current_base.getFactionName()))
    trace(_trace_level, repr( prices ))

    return prices, exports

def get_player_manifest(prices):
    imports = []
    not_for_sale = []
    player = VS.getPlayer()
    
    count_not_for_sale = 0
    for i in range(player.numCargo()):
        cargo    = player.GetCargoIndex(i)
        name     = cargo.GetContent()
        category = cargo.GetCategory()
        quantity = cargo.GetQuantity()

        if name == '': continue
        if category[:8] == 'upgrades': continue
        if category[:9] == 'starships': continue

        not_ok_to_sell = 0
        try:
            # only add item if it is on the price list for this planet/station/outpost
            price = prices[name]
            imports.append([name, quantity])
        except:
            not_ok_to_sell = 1
            count_not_for_sale += quantity

        if (not_ok_to_sell):
            try:
                not_for_sale.append([name, quantity])
            except:
                pass

    trace(_trace_level, "::: imports ")
    trace(_trace_level, (repr( imports )))
    trace(_trace_level, "::: not_for_sale cargo ")
    trace(_trace_level, (repr( not_for_sale )))

    return imports, count_not_for_sale

def transfer_cargo(from_unit, to_unit, name, price, count, max_capacity=-1, current_capacity=0):
    trace(_trace_level, "::: transfer_cargo(%s, %s, %s, %s, %s, %s, %s)" %(from_unit.getName(), to_unit.getName(), name, price, count, max_capacity, current_capacity))
    if (count <= 0):
        return 0

    if (max_capacity > 0):
        trace(_trace_level, "::: max capacity = %s" %(max_capacity))
        # only player ships should have a max_capacity; bases & planets can accept lots of cargo
        if (current_capacity >= max_capacity): 
            # unit is full (or overloaded) already
            return 0

        if (count > (max_capacity - current_capacity)):
            # if adding requested amount would overfill capacity, reduce it to an OK level
            count = max_capacity - current_capacity
        
    if (from_unit.hasCargo(name)):
        trace(_trace_level, "::: from_unit has cargo" )
        # make sure that from_unit actually has the cargo we're transferring
        cargo_obj = from_unit.GetCargo(name)
        from_count = cargo_obj.GetQuantity()
        if (from_count <= 0):
            # if they have no cargo, skip the rest of subroutine
            return 0
        if (count > from_count):
            # if they don't have enought, reduce it to OK level
            count = from_count
        # finally, remove cargo from this unit
        from_unit.removeCargo(name,count,True)    # the last param is erasezero, meaning erase from cargo list if zero?
    else:
        trace(_trace_level, "::: from_unit DOESN'T have cargo" )
        return 0        
    
    # lastly, add [count] cargo to new unit
    #    create a new Cargo object and add it to unit
    #    VS.Cargo __init__ appears to use: Content, Category, Price, Quantity, Mass, Volume
    cargo_obj = VS.Cargo(name, name, price, count, 0.01, 1.0)
    cargo_obj.SetMaxFunctionality(1.0)
    cargo_obj.SetFunctionality(1.0)
    to_unit.addCargo(cargo_obj)

    return count


def get_sprite_info():
    info = {
        'Advanced_Fuels':        'interfaces/commodity/cargo/advanced-fuels.spr',
        'Artwork':                'interfaces/commodity/cargo/artwork.spr',
        'Books':                'interfaces/commodity/cargo/books.spr',
        'Communications':        'interfaces/commodity/cargo/communications.spr',
        'Computers':            'interfaces/commodity/cargo/computers.spr',
        'Brilliance':            'interfaces/commodity/cargo/brilliance.spr',
        'Pilot':                'interfaces/commodity/cargo/slaves.spr',
        'Slaves':                'interfaces/commodity/cargo/slaves.spr',
        'Tobacco':                'interfaces/commodity/cargo/tobacco.spr',
        'Ultimate':                'interfaces/commodity/cargo/ultimate.spr',
        'Construction':            'interfaces/commodity/cargo/construction.spr',
        'Factory_Equipment':    'interfaces/commodity/cargo/factory-equipment.spr',        
        'Food_Dispensers':        'interfaces/commodity/cargo/food-dispensers.spr',
        'Furs':                    'interfaces/commodity/cargo/furs.spr',
        'Games':                'interfaces/commodity/cargo/games.spr',
        'Gems':                    'interfaces/commodity/cargo/gems.spr',
        'Generic_Foods':        'interfaces/commodity/cargo/generic-foods.spr',
        'Grain':                'interfaces/commodity/cargo/grain.spr',
        'Holographics':            'interfaces/commodity/cargo/holographics.spr',
        'Home_Appliances':        'interfaces/commodity/cargo/home-appliances.spr',
        'Home_Entertainment':    'interfaces/commodity/cargo/home-entertainment.spr',
        'Iron':                    'interfaces/commodity/cargo/iron.spr',
        'Liquor':                'interfaces/commodity/cargo/liquor.spr',
        'Luxury_Foods':            'interfaces/commodity/cargo/luxury-foods.spr',
        'Medical_Equipment':    'interfaces/commodity/cargo/medical-equipment.spr',
        'Mining_Equipment':        'interfaces/commodity/cargo/mining-equipment.spr',
        'Movies':                'interfaces/commodity/cargo/movies.spr',
        'Pets':                    'interfaces/commodity/cargo/pets.spr',
        'Plastics':                'interfaces/commodity/cargo/plastics.spr',
        'PlayThing_(tm)':        'interfaces/commodity/cargo/plaything.spr',
        'Plutonium':            'interfaces/commodity/cargo/plutonium.spr',
        'Pre_Fabs':                'interfaces/commodity/cargo/pre-fabs.spr',
        'Robot_Servants':        'interfaces/commodity/cargo/robot-servants.spr',
        'Robot_Workers':        'interfaces/commodity/cargo/robot-workers.spr',
        'Software':                'interfaces/commodity/cargo/software.spr',
        'Space_Salvage':        'interfaces/commodity/cargo/space-salvage.spr',
        'Textiles':                'interfaces/commodity/cargo/textiles.spr',
        'Tungsten':                'interfaces/commodity/cargo/tungsten.spr',
        'Uranium':                'interfaces/commodity/cargo/uranium.spr',
        'Weaponry':                'interfaces/commodity/cargo/weaponry.spr',
        'Wood':                    'interfaces/commodity/cargo/wood.spr'
        }
    return info
    
def get_display_name(name):
    if (name == 'Contraband/Pilot'):
        return 'Slaves (pilot)'
    elif (name[0:10] == 'Contraband'):
        return name[11:]
    return name.replace('_', ' ')
