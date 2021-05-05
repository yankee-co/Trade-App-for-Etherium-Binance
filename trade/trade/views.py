from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .config import API_KEY, SECRET_KEY

from binance.client import Client
from binance.enums import *

from .forms import Quantity_buy, Sell_Price

import math
import requests
import json
import csv
from datetime import datetime
import time

client = Client(API_KEY, SECRET_KEY)

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def sell_session_vars(request):
    request.session['quantity_buy'] = 0
    request.session['spent'] = 0
    request.session['bnb_prices'] = []
    request.session['orderId'] = False
    request.session['order'] = False

def check_active_limit(request):
    active_limit_orders = client.get_open_orders(symbol='BNBUSDT')
    if not active_limit_orders and request.session['order']:
        sell_session_vars(request)

def new_limit(request, price_sell):
    order = client.order_limit_sell(
        symbol='BNBUSDT',
        quantity=request.session['quantity_buy'],
        price=price_sell)
    
    request.session['orderId'] = order['orderId']
    request.session['order'] = order

def destroy_active_limit(request):
    result = client.cancel_order(
        symbol = 'BNBUSDT',
        orderId = request.session['orderId'])

    check_active_limit(request)

class MainView(TemplateView):
    def get(self, *args, **kwargs):

        info = client.get_symbol_info('BNBUSDT')
        client_info = client.get_account()
        
        dicted_balances = client_info['balances']
        balances = [{'asset':balance['asset'],'free':balance['free']} for balance in dicted_balances if balance['free'] != '0.00000000' and balance['free'] != '0.00']

        spent = self.request.session.get('spent', False)
        quantity_buy = self.request.session.get('quantity_buy', False)
        bnb_prices = self.request.session.get('bnb_prices', False)
        order = self.request.session.get('order', False)
        BNBUSDT_price = client.get_margin_price_index(symbol='BNBUSDT')['price']
        limit_default = str(truncate(float(BNBUSDT_price) + float(BNBUSDT_price)*0.1, 2))
        total_p_l = self.request.session.get('total_p_l', False)

        if order:
            order_data = {
                'Symbol': order['symbol'],
                'TransactTime': datetime.fromtimestamp(int(str(order['transactTime'])[0:-3])).strftime('%Y-%m-%d %H:%M:%S') + " UTC",
                'Price': order['price'],
                'Quantity': order['origQty'],
                'Status': order['status'],
            }
        else:
            order_data = {}

        if bnb_prices:
            average_price = sum(bnb_prices)/len(bnb_prices)
            price_change = truncate(float(BNBUSDT_price)/average_price * 100, 2)
        else:
            average_price = 0
            price_change = 0

        if not spent == False and float(spent) > 0:
            dollars_change = truncate((price_change/100)*float(spent), 2)
        else:
            dollars_change = 0

        if bnb_prices:
            limit_bought_change = truncate(float(limit_default)/average_price*100, 2)
        else:
            limit_bought_change = 0

        check_active_limit(self.request)

        context = {
            'dollars_change':dollars_change,
            'balances': balances,
            'limit_default':limit_default,
            'quantity_buy':quantity_buy,
            'spent':spent,
            'average_price':average_price,
            'limit_bought_change':limit_bought_change,
            'order_data':order_data,
            'order':order,
            'total_p_l':total_p_l,
        }

        return render(
            self.request, 'main.html', context
        )


def buy(request):
    
    orders = client.get_all_orders(symbol = 'BNBUSDT')
    context = {}

    if request.method == 'POST':
        form = Quantity_buy(request.POST)

        if form.is_valid():
            try:
                order = client.order_market_buy(
                    symbol='BNBUSDT',
                    quantity = form.cleaned_data['quantity_buy']
                )

                if 'bnb_prices' not in request.session:
                    request.session['bnb_prices'] = []

                if float(request.session['quantity_buy']) > 0: request.session['quantity_buy'] += truncate((float(order['executedQty']) - float(order['fills'][0]['commission'])), 6)
                else: request.session['quantity_buy'] = truncate((float(order['executedQty']) - float(order['fills'][0]['commission'])), 6) 
 
                if float(request.session['spent']) > 0: request.session['spent'] += truncate(float(order['cummulativeQuoteQty']), 2)
                else: request.session['spent'] = truncate(float(order['cummulativeQuoteQty']), 2)

                request.session['bnb_prices'].append(truncate(float(order['fills'][0]['price']), 2))

                context.update({'gained':form.cleaned_data['quantity_buy'], 'lost':order['cummulativeQuoteQty']})
                
                print(order, '  ', request.session['quantity_buy'])

            except Exception as e:
                return render(request, 'buy.html', {'exception':e})

        else:
            form = Quantity()

    return render(request, 'buy.html', context)
    
def sell_market(request):

    context = {}

    if request.method == 'POST':

        try:
            if request.session['orderId']:
                destroy_active_limit(request)

            order = client.order_market_sell(
                symbol = 'BNBUSDT',
                quantity = request.session['quantity_buy'])
    
            context.update({'lost':request.session['quantity_buy'], 'gained':order['cummulativeQuoteQty']})
            
            sell_session_vars(request)

        except Exception as e:
            context.update({'exception':e})
            
    return render(request, 'sell_market.html', context)

    

def sell_limit(request):

    context = {}

    if request.method == 'POST':

        form = Sell_Price(request.POST)

        if form.is_valid():

            try:
                price_sell = (form.cleaned_data['value0']+form.cleaned_data['value1']+form.cleaned_data['value2']+form.cleaned_data['value3']+form.cleaned_data['value4']+form.cleaned_data['value5'])

                if not request.session['orderId']:
                    new_limit(request, price_sell)

                if request.session['orderId']:
                    destroy_active_limit(request)
                    new_limit(request, price_sell)

            except Exception as e:
                return render(request, 'sell_limit.html', {'exception':e})

    return render(request, 'sell_limit.html', context)





# Spot API URL                              Spot Test Network URL


# https://api.binance.com/api	            https://testnet.binance.vision/api/v3/userDataStream

# wss://stream.binance.com:9443/ws	        wss://testnet.binance.vision/ws

# wss://stream.binance.com:9443/stream	    wss://testnet.binance.vision/stream


# {'symbol': 'SOLUSDT',

# 'orderId': 296002485,

# 'orderListId': -1,

# 'clientOrderId': 'XMRHS3kvGmiJckQVyBdYmZ',

# 'transactTime': 1619789018258,

# 'price': '0.00000000',

# 'origQty': '0.38000000',

# 'executedQty': '0.38000000',

# 'cummulativeQuoteQty': '16.41752000',

# 'status':'FILLED',

# 'timeInForce': 'GTC',

# 'type': 'MARKET',

# 'side': 'BUY',

# 'fills': [{'price': '43.20400000', 'qty': '0.38000000', 'commission': '0.00002025', 'commissionAsset': 'BNB', 'tradeId': 21763303}]}
