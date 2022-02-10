from django.shortcuts import render
import requests
import json
import re

url = "https://api.zksync.io/api/v0.2/fee"
 
headers = {
    "Content-Type": "application/json"
}

# Layer 2 to Layer 2 Transfer

def Layer2toLayer2():
    payload_l2_l2_T = {
    "txType": "Transfer",
    "address": "0xf33A2D61DD09541A8C9897D7236aDcCCC14Cf769",
    "tokenLike": "USDT",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "txType": {
        "anyOf": [
            {
            "type": "string",
            "enum": [
                "Transfer"
            ]
            },
            {
            "type": "object",
            "properties": {
                "ChangePubKey": {
                "type": "string",
                "enum": [
                    "Onchain",
                    "ECDSA",
                    "CREATE2"
                ]
                }
            },
            "required": [
                "ChangePubKey"
            ],
            "enum": [
                {
                "ChangePubKey": "Onchain"
                },
                {
                "ChangePubKey": {
                    "onchainPubkeyAuth": False
                }
                }
            ]
            }
        ]
        },
        "address": {
        "type": "string"
        },
        "tokenLike": {
        "anyOf": [
            {
            "type": "number"
            },
            {
            "type": "string",
            "enum": [
                "ETH"
            ]
            }
        ]
        }
    },
    "required": [
        "txType",
        "address",
        "tokenLike"
    ]
    }

    L2_t_L2_T = requests.post(url, data=json.dumps(payload_l2_l2_T), headers=headers)

    regex = """(?<="totalFee":")(.*)(?="}})"""
    L1_t_L2_T_f = re.findall(regex,L2_t_L2_T.text)
    fees = (L1_t_L2_T_f[0])

    return fees


# Layer 2 to Layer 2 Transfer

def Layer1toLayer2():
    payload_l1_l2_W = {
    "txType": "Withdraw",
    "address": "0xf33A2D61DD09541A8C9897D7236aDcCCC14Cf769",
    "tokenLike": 0,
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "txType": {
        "anyOf": [
            {
            "type": "string",
            "enum": [
                "Withdraw"
            ]
            },
            {
            "type": "object",
            "properties": {
                "ChangePubKey": {
                "type": "string",
                "enum": [
                    "Onchain",
                    "ECDSA",
                    "CREATE2"
                ]
                }
            },
            "required": [
                "ChangePubKey"
            ],
            "enum": [
                {
                "ChangePubKey": "Onchain"
                },
                {
                "ChangePubKey": {
                    "onchainPubkeyAuth": False
                }
                }
            ]
            }
        ]
        },
        "address": {
        "type": "string"
        },
        "tokenLike": {
        "anyOf": [
            {
            "type": "number"
            },
            {
            "type": "string",
            "enum": [
                "ETH"
            ]
            }
        ]
        }
    },
    "required": [
        "txType",
        "address",
        "tokenLike"
    ]
    }

    L1_t_L2_W = requests.post(url, data=json.dumps(payload_l1_l2_W), headers=headers)

    regex = """(?<="totalFee":")(.*)(?="}})"""
    L1_t_L2_T_f = re.findall(regex,L1_t_L2_W.text)
    fees = (L1_t_L2_T_f[0])
    return  fees 

def getETHprice():
    eth_price_res = requests.get("https://api.zksync.io/api/v0.2/tokens/0/priceIn/usd")
    eth_price_pattern = """(?<="price":")(.*)(?="}})"""
    eth_price_res = re.findall(eth_price_pattern, eth_price_res.text)[0]
    
    return eth_price_res

def addValues(x, y):
    # print(x, y)
    result = int(float((x[0:8]))) * int(float((y[0:8])))
    return result / 10000000000


def getEthFees():
    url = "https://ethgas.watch/api/gas"
    x = requests.get(url)

    gasjson = json.loads(x.text)
    slow = gasjson["slow"]["usd"]
    normal = gasjson["normal"]["usd"]
    fast = gasjson["fast"]["usd"]
    instant = gasjson["instant"]["usd"]

    return slow, normal, fast, instant

def home(request):
    Ethfees = getETHprice()
    l2tl2 = Layer2toLayer2()
    l1tl2 = Layer1toLayer2()
    l2tl2_total = addValues(l2tl2, Ethfees)
    l1tl2_total = addValues(l1tl2, Ethfees)
    slow, normal, fast, instant = getEthFees()
       
    return render(request, 'home.html', {"l2l2p": l2tl2_total, "l1l2p": l1tl2_total, "slow": slow, "fast": fast, "instant": instant, "normal": normal})


def test(request):
    return render(request, 'home.html')