from telegram import *
from telegram.ext import *
import requests
import json
from pycoingecko import CoinGeckoAPI
import sched, time
from threading import Timer

cg = CoinGeckoAPI()
#Insert Bot Token
bot = Bot("XXXXXXXXXXXXXXXXXXXXXX")
counter=0
        

def fetch():
    global bot
    global counter
    counter+=1
    
    #Get SCH ticker from XBTS
    schresponse = requests.get("https://api.xbts.io/api/ticker/sch_sky")
    
    #Get Skycoin price from CoinGecko
    skyprice = cg.get_price(ids='skycoin', vs_currencies='usd')
    skyprice = (skyprice['skycoin']['usd'])
    print(skyprice)

    #Transform call into json / dict
    schresponsejson = schresponse.json()
    print(schresponsejson)
        
    #XBTS SCH Metrics
    sch_Price = float(schresponsejson['SCH_SKY']['last'])
    sch_High = str(schresponsejson['SCH_SKY']['high'])
    sch_low = str(schresponsejson['SCH_SKY']['low'])
        
    print(sch_Price)

    #Math for USD 
    sch_usd = sch_Price * skyprice
   
    #Avoid Scnentific Notation
    sch_usd = f'{sch_usd:.10f}'
    sch_Price = f'{sch_Price:.6f}'

    #Coinhour math
    sch_year = 24*365

    #Telegram Bot set-up
    #Insert Bot token
    updater=Updater("XXXXXXXXXXXXXXXXXXX", use_context=True)
    dispatcher=updater.dispatcher

    def sch_metrics(update:Update, context:CallbackContext):
        bot.send_message(
            chat_id=update.effective_chat.id,
            text= "Exchange: XBTS\n\nTicker: SCH/SKY\nLast price: " +str(sch_Price)+ "\n" + "24h High: "+ sch_High + "\n" + "24h low: " + sch_low +"\n \n"+ "Ticker: SCH/USD " +"\n" "Last price: " + str(sch_usd)
        )

    #Staking Math
    sky_yearlystaking= float(sch_year) * float(sch_Price) / 100
    usd_yearlystaking = float(sch_year) * float(sch_usd)

    #Avoid Scientific Notation
    sky_yearlystaking = f'{sky_yearlystaking:.12f}'
    usd_yearlystaking = f'{usd_yearlystaking:.8f}'

    #Set up for/schprice
    def sky_apy(update:Update, context:CallbackContext):
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Holding 1 Skycoin for a year (at current SCH prices) will yield: \n\nCoin Hours: "+str(sch_year)+ "\n" +"Skycoin: "+str(sky_yearlystaking)+ "%" + "\n"+"USD: "+ str(usd_yearlystaking) 
        )

    start_value=CommandHandler('skystaking',sky_apy)
    dispatcher.add_handler(start_value)

    start_value=CommandHandler('schprice', sch_metrics)
    dispatcher.add_handler(start_value)

    if counter == 1:
        updater.start_polling()    
    
    Timer(5, fetch).start()
    
fetch()
