from flask import Flask, render_template
import requests as req
import json
from flask import jsonify
import datetime

# variables
wrx_url='https://api.wazirx.com/api/v2/tickers'
binance_url= 'https://api.binance.com/api/v3/ticker/price'
dcx_url='https://api.coindcx.com/exchange/ticker'

app = Flask(__name__)

# venv\Scripts\activate
# Members api Route
#urls or mappings
@app.route('/')
def home_url():

    data_b_w=format_binance_wrx_data()
    sorted_list=sorted(data_b_w, key = lambda i: i['%diff'])
    sorted_list.reverse()
    return render_template('index.html', data=sorted_list)

@app.route('/arb')
def arb_fn():
    return json.dumps(combine_data())

@app.route('/arb/diff')
def arb_diff():
    return str(diff_data())
    # json.dumps(diff_data())


@app.route('/arb/diff/sorted')
def arb_diff_str():
    json_data=diff_data()
    o_dict=dict(reversed(sorted(json_data.items(), key=lambda item: item[1])))
    lst_sorted=list()
    for key,val in  o_dict.items():
        lst_sorted.append({key:val})

    return jsonify({'wrx-DCX-data':lst_sorted})


# Delete this
@app.route("/list")
def data_list():
    return {'data':[1,2,3,6,9,0]}

#------------------- sort data



def get_wrx_data():
    wres=req.get(wrx_url)
    wrx_data=dict()
    for key , val in wres.json().items():
        if 'inr' in key or 'usdt' in key:
            wrx_data[key.upper()]=val['last']
    return wrx_data

def get_dcx_data():
    dcx_data=dict()
    dres=req.get(dcx_url)
    dval=dres.json()[:-1] # Removing last element
    for el in dval:
        if 'INR' in el['market']  or 'USDT' in  el['market'] :
            dcx_data[el['market'].upper()]=el['last_price']
    return dcx_data

def combine_data():
    #get data to process
    wrx_data=get_wrx_data()
    dcx_data=get_dcx_data()
    common_keys= list(set(wrx_data.keys()).intersection(set(dcx_data.keys())))
    common_keys.sort()
    wrx_c_data=dict()
    dcx_d_data=dict()
    for ll in common_keys:
        wrx_c_data[ll]=wrx_data[ll]
        dcx_d_data[ll]=dcx_data[ll]

    response_data= [{'waxirx': wrx_c_data},{'coinDCX': dcx_d_data }]
    return response_data

def diff_data():
    json_data=combine_data()

    waxirx  = json_data[0]['waxirx']
    coinDCX = json_data[1]['coinDCX']
    diff_list=dict()
    for k in waxirx.keys():
        wp= float(waxirx[k])
        dp=  float(coinDCX[k])
        prec= 0
        if wp > 0 and dp > 0:
            diff= abs(wp-dp)
            prec = round((diff*100) /(min(wp,dp)), 3)

        diff_list[k]= prec


    # diff_list.sort()
    # diff_list.reverse()
    return diff_list

#-------------------- Binance-wrx functions

def get_binance_usdt():
    bres=req.get(binance_url)
    binance_data=dict()
    # print(bres.json())
    for ticker in bres.json():
    #     print(ticker)
        if 'USDT' in ticker['symbol']:
            binance_data[ticker['symbol'].upper()]=ticker['price']
    #         print(ticker['symbol'])
    #         print(binance_data[ticker['symbol'].upper()])
    return binance_data

def get_bin_wrx_comm_usdt():
    common_list=list()

    wrx_data=get_wrx_usdt()
    binance_data=get_binance_usdt()
    for key in binance_data:
        if key in wrx_data:
            common_list.append(key)

    return common_list

def format_binance_wrx_data():
    data_dict_bin_wrx= list()
    wrx_usdt=get_wrx_usdt()
    bin_usdt=get_binance_usdt()

    common_list=get_bin_wrx_comm_usdt()
    for symbol in common_list:
        diff= float(bin_usdt[symbol])  - float(wrx_usdt[symbol])
        if(float(wrx_usdt[symbol])== 0):
            continue
    #         print("wrx 0")

            wrx_usdt[symbol]=float(wrx_usdt[symbol])+0.0000000001
        pct=(diff/float(wrx_usdt[symbol]))*100

    #     if(diff>1):
    # #         print(round(pct,4), "<b>  |||||||||||</b>",symbol )
    # #     print(diff,symbol, pct)
        data={
            'symbol': symbol,
            'info': 'binance - wazirx    (usdt price)',
            'diff': diff,
            '%diff': round(pct,3),
            'timestamp': str(datetime.datetime.now()),
            'prices': {
                'wrx':  wrx_usdt[symbol] ,
                'bin':  bin_usdt[symbol]}
             }
        data_dict_bin_wrx.append(data)
    return data_dict_bin_wrx


def get_wrx_usdt():
    wres=req.get(wrx_url)
    wrx_data=dict()
    for key , val in wres.json().items():
        if  'usdt' in key:
            wrx_data[key.upper()]=val['last']
    return wrx_data


if __name__ == "__main__":
    app.run(debug=True)
