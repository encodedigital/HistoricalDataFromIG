import config
import database
import requests
import json

baseURL = 'https://demo-api.ig.com/gateway/deal'

def igLogin():
    loginURL = baseURL + '/session'
    params = {
        "identifier": config.igUsername,
        "password": config.igPassword
    }
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json; charset=UTF-8",
        "X-IG-API-KEY": config.igApiKey,
        "Version": "1"
    }
    response = requests.post(loginURL, json=params, headers=headers)

    result = {
        "CST": response.headers['CST'],
        "X-SECURITY-TOKEN": response.headers['X-SECURITY-TOKEN']}
    return result

def igHistoricalPrices(loginTokens, forexPair, dataTimeframe, dataPoints):

    epic = "CS.D."+forexPair+".TODAY.IP"
    resolution = dataTimeframe
    numPoints = dataPoints

    priceURL = baseURL + "/prices/" + epic + "/" + resolution + "/" + numPoints

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json; charset=UTF-8",
        "X-IG-API-KEY": config.igApiKey,
        "Version": "1",
        "CST": loginTokens["CST"],
        "X-SECURITY-TOKEN": loginTokens["X-SECURITY-TOKEN"]
    }

    response = requests.get(priceURL, headers=headers)
    tempData = json.loads(response.text)

    dataResult = []
    for d in tempData["prices"]:
        snapshotTime = d["snapshotTime"]
        open_ask = d["openPrice"]["ask"]
        open_bid = d["openPrice"]["bid"]
        close_ask = d["closePrice"]["ask"]
        close_bid = d["closePrice"]["bid"]
        high_ask = d["highPrice"]["ask"]
        high_bid = d["highPrice"]["bid"]
        low_ask = d["lowPrice"]["ask"]
        low_bid = d["lowPrice"]["bid"]

        dataResult.append([snapshotTime, open_ask, open_bid, close_ask, close_bid, high_ask, high_bid, low_ask, low_bid])

    return dataResult

if __name__ == '__main__':
    try:
        forexPair = input("Enter Forex Pair:")
        #DAY, WEEK, MONTH, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, 
        #MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4
        dataTimeframe = input("Choose Data Timeframe: ")
        dataPoints = input("How much data in "+dataTimeframe+"s:")
        
        loginTokens = igLogin()
        dataResult = igHistoricalPrices(loginTokens, forexPair.upper(), dataTimeframe.upper(), dataPoints)

        tableName = forexPair.upper() + "_" + dataTimeframe.upper()
        database.loadData(tableName, dataResult)

    except Exception as e:
        print(e)