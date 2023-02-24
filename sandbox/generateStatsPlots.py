import numpy as np
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch

es = Elasticsearch(os.environ['ELASTICSEARCH_HOST'])
indicesList = ["daily_btc", "daily_eth", "daily_bnb"]
coinsList = ["BTC", "ETH", "BNB"]
colorsList = ["blue", "yellow", "red"]

def getAvgPrice(i):
    return i["_source"]["avgPrice"]

def getPriceVariation(i):
    return i["_source"]["priceVariation"]

def getLogAvgPrice(i):
    return i["_source"]["LogAvgPrice"]
def getDevVW(i):
    return i["_source"]["deviationVariationWeek"] if "deviationVariationWeek" in i["_source"] else 0
def getIncreaseDay(i):
    return 1 if i["_source"]["increaseDay"] else 0
def getIncreaseWeek(i):
    return i["_source"]["increasePercentWeek"] if "increasePercentWeek" in i["_source"] else 0.5
def getIncreaseMonth(i):
    return i["_source"]["increasePercentWeightedMonth"] if "increasePercentWeek" in i["_source"] else 0.5

def getVector(values, f):
    vectorizeNpFunction = np.vectorize(f)
    return vectorizeNpFunction(values)


for i in range(len(indicesList)):
    data = es.search(index=indicesList[i], query={"match_all": {}}, size=10000)
    data = data['hits']['hits']
    #############
    # vDataAvgPrice = getVector(data, getAvgPrice)
    # plt.title("Визуализация частот значений средних цен (" + coinsList[i] + ")")
    # plt.hist(vDataAvgPrice, bins=100, color=colorsList[i])
    # plt.xlabel('Average price')
    # plt.ylabel('Frequency')
    # plt.savefig("./sandbox/tmp/" + coinsList[i] + "_avgPrice.png")
    # plt.clf()
    #############
    vDataAvgPrice = getVector(data, getPriceVariation)
    plt.title("Визуализация разброса суточных колебаний цен (" + coinsList[i] + ")")
    plt.hist(vDataAvgPrice, bins=100, color=colorsList[i])
    plt.xlabel('Price variation')
    plt.ylabel('Frequency')
    plt.savefig("./sandbox/tmp/" + coinsList[i] + "_priceVariation.png")
    plt.clf()
    #############
    vDataAvgPrice = getVector(data, getLogAvgPrice)
    plt.title("Визуализация разброса логарифма колебаний цен (" + coinsList[i] + ")")
    plt.hist(vDataAvgPrice, bins=100, color=colorsList[i])
    plt.xlabel('log(Average price)')
    plt.ylabel('Frequency')
    plt.savefig("./sandbox/tmp/" + coinsList[i] + "_logAvgPrice.png")
    plt.clf()
    #############
    vDataAvgPrice = getVector(data, getDevVW)
    plt.title("Визуализация разброса std колебаний цен (" + coinsList[i] + ")")
    plt.hist(vDataAvgPrice, bins=100, color=colorsList[i])
    plt.xlabel('std(price variations week)')
    plt.ylabel('Frequency')
    plt.savefig("./sandbox/tmp/" + coinsList[i] + "_stdPriceVariation.png")
    plt.clf()
    #############
    vDataAvgPrice = getVector(data, getIncreaseDay)
    plt.title("Визуализация соотношения дней роста и падения (" + coinsList[i] + ")")
    plt.hist(vDataAvgPrice, bins=2, color=colorsList[i])
    plt.xlabel('decrease/increase')
    plt.ylabel('Frequency')
    plt.savefig("./sandbox/tmp/" + coinsList[i] + "_increase.png")
    plt.clf()
    #############
    vDataAvgPrice = getVector(data, getIncreaseWeek)
    plt.title("Визуализация сохранения тренда дней роста и падения за неделю (" + coinsList[i] + ")")
    plt.hist(vDataAvgPrice, bins=50, color=colorsList[i])
    plt.xlabel('decrease streak --> 0')
    plt.ylabel('Frequency')
    plt.savefig("./sandbox/tmp/" + coinsList[i] + "_increaseWeek.png")
    plt.clf()
    #############
    vDataAvgPrice = getVector(data, getIncreaseMonth)
    plt.title("Визуализация сохранения взвешенного тренда дней роста и падения за месяц (" + coinsList[i] + ")")
    plt.hist(vDataAvgPrice, bins=50, color=colorsList[i])
    plt.xlabel('decrease streak --> 0')
    plt.ylabel('Frequency')
    plt.savefig("./sandbox/tmp/" + coinsList[i] + "_increaseMonth.png")
    plt.clf()


