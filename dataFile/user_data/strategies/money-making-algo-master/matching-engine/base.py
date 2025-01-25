
class OrderBook(object):
    """ 
    Holds all orders
    """
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.order_id_map = {}

class Orders(object):
    """
    Order object for input into orderbook
    """
    def __init___(self, pair, order_type, price, qty, side, order_id):
        self.pair = pair
        self.order_type = order_type
        self.price = price
        self.qty = qty
        self.side = side
        self.order_id = order_id

class Cancel(object):
    """
    Cancelation object to remove orders form order book
    """
    def __init_(self, order_id, side, cancel_price, cancel_qty ):
        self.order_id = order_id
        self.side = side
        self.cancel_price = cancel_price
        self.cancel_qty = cancel_qty

class Match(object):

    def __init__(self, order_ids, match_price, match_qty):
        # order_ids is a list of two orders. Index 0 is the bid, 1 is the ask
        self.order_ids = order_ids
        self.match_price = match_price
        self.match_qty = match_qty

class BaseEngine(object):
    """
    Base Engine for various exchange data inputs
    """
    def __init__(self):
        self.order_book = OrderBook()
        self.curr_order_id = 0 
        self.curr_trade_id = 0
    
    def add_order(self, order):
        """
        Inputs an order to be added to the orderbook
        :param order   An order object containing all attributes
        :return   200 if successful 100 if not
        """
        if order.side == 0:
            #meaning 0 == bid
            self.order_book.bids[order.order_id] = order
            return 200
        elif order.side == 1:
            #meaning ask
            self.order_book.asks[order.order_id] = order
            return 200
        
        return 100
    
    def cancel_order(self, cancel):
        """
        Inputs a Cancel to remove an order from the book
        """
        if cancel.side == 0:
            if cancel.order_id in self.order_book.bids:
                self.order_book.bids.pop(cancel.order_id)
        elif cancel.side == 1:
            if cancel.order_id in self.order_book.asks:
                self.order_book.asks.pop(cancel.order_id)
    
    def match_order(self, match):

        bid = self.order_book.bids.pop(match.order_ids[0])
        ask = self.order_book.asks.pop(match.order_ids[1])

        if bid.qty == ask.qty:
            return 200
        elif bid.qty > ask.qty:
            bid.qty = bid.qty - ask.qty
            self.add_order(bid)
        else:
            ask.qty = ask.qty - bid.qty
            self.add_order(ask)


    