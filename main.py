import matplotlib.pyplot as plot
import pandas as pd
from datetime import datetime, timedelta


def openFile(filename):
    fileOpen = open(filename)
    content = fileOpen.read()
    fileOpen.close()
    return content.split()


# storing data per days in dictionary


def daysDictionary(content, ignoreLine, price=1):
    day = 0
    revenueDict = {}
    content = content[ignoreLine:]
    for i in range(len(content) - 1, -1, -1):
        d = datetime.today() - timedelta(days=day)
        revenueDict[str(d)[:10]] = [int(content[i]) * price, d.weekday()]
        day += 1

    return revenueDict


def yearlyRev(dictVal):
    resultDate = []
    resultVal = []
    total = 0
    resultDict = {}

    for i in dictVal.keys():
        if i[:4] not in resultDate:
            resultDate.append(i[:4])
            if (len(resultDate) > 1):
                resultVal.append(total)
                total = 0
        total = total + int(dictVal[i][0])
    else:
        resultVal.append(total)

    resultDict["Year"] = resultDate
    resultDict["Total"] = resultVal

    return resultDict


def weeklyRev(dictVal):
    resultDate = []
    resultVal = []
    total = 0
    resultDict = {}
    week = ""
    j = 0

    for i in dictVal.keys():
        if (j == 0 and dictVal[i][1] != 6):
            week = week + i[:10]

        elif (dictVal[i][1] == 6):
            week = week + i[:10]

        elif (dictVal[i][1] == 0):
            week = week + "~" + i[:10]

        total = total + int(dictVal[i][0])

        if (len(week) > 12):
            resultDate.append(week)
            resultVal.append(total)
            week = ''
            total = 0

        j = j + 1

    resultDict["Week"] = resultDate
    resultDict["Total"] = resultVal

    return resultDict


def monthlyRev(dictVal):
    resultDate = []
    resultVal = []
    total = 0
    resultDict = {}

    for i in dictVal.keys():
        if i[:7] not in resultDate:
            resultDate.append(i[:7])
            if (len(resultDate) > 1):
                resultVal.append(total)
                total = 0
        total = total + int(dictVal[i][0])
    else:
        resultVal.append(total)

    resultDict["Month"] = resultDate
    resultDict["Total"] = resultVal

    return resultDict


def customInterval(dictVal, startDate, stopDate):
    resultDate = []
    resultVal = []
    resultDict = {}
    startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
    stopDate = datetime.strptime(stopDate, '%Y-%m-%d').date()

    if (startDate > stopDate):

        for i in dictVal.keys():
            listDate = datetime.strptime(i[:10], '%Y-%m-%d').date()
            if (startDate >= listDate >= stopDate):
                resultDate.append(i[:10])
                resultVal.append(int(dictVal[i][0]))

        resultDict["Day"] = resultDate
        resultDict["Total"] = resultVal
    else:
        resultDict = "[Incorrect date interval.]"

    return resultDict


def showGraphYear(revenueOpt, titleOpt):
    revenue = yearlyRev(revenueOpt)
    dataFrame = pd.DataFrame(data=revenue)
    dataFrame.plot.bar(x="Year", y="Total", rot=70, title=titleOpt)
    plot.show(block=True)


def showGraphWeekly(revenueOpt, titleOpt):
    revenue = weeklyRev(revenueOpt)
    dataFrame = pd.DataFrame(data=revenue)
    dataFrame.plot.bar(x="Week", y="Total", rot=70, title=titleOpt)
    plot.show(block=True)


def showGraphMonthly(revenueOpt, titleOpt):
    revenue = monthlyRev(revenueOpt)
    dataFrame = pd.DataFrame(data=revenue)
    dataFrame.plot.bar(x="Month", y="Total", rot=70, title=titleOpt)
    plot.show(block=True)


def showGraphCustom(revenueOpt):
    start = input("Enter start date in format yyyy-mm-dd: ")
    stop = input("Enter stop date in format yyyy-mm-dd: ")
    revenueCustom = customInterval(revenueOpt, start, stop)
    if (type(revenueCustom) != str):
        dataFrame = pd.DataFrame(data=revenueCustom)
        dataFrame.plot.bar(
            x="Day",
            y="Total",
            rot=70,
            title="Custom interval cupcakes revenue")
        plot.show(block=True)
    else:
        print(revenueCustom)


def compareGraph(revenueOpt1, revenueOpt2):
    start = input("Enter start date in format yyyy-mm-dd: ")
    stop = input("Enter stop date in format yyyy-mm-dd: ")
    newData = {}

    revenueCustom1 = customInterval(revenueOpt1, start, stop)
    revenueCustom2 = customInterval(revenueOpt2, start, stop)

    newData["Basic cupcakes"] = revenueCustom1["Total"]
    newData["Delux cupcakes"] = revenueCustom2["Total"]
    indexData = revenueCustom1["Day"]

    dataFrame = pd.DataFrame(
        data=newData, index=indexData)

    dataFrame.plot.bar(
        rot=15, title="Basic cupcakes Revenue vs Delux cupcakes revenue")

    plot.show(block=True)


def subOption():
    print("[a] [Total revenue.]")
    print("[b] [Basic cupcakes revenue.]")
    print("[c] [Delux cupcakes revenue.]")

    print("[x] [To return]")

    option = input("Select option: ")

    return option


if __name__ == "__main__":
    fileNames = ['Basic.txt', 'Delux.txt', 'Total.txt']
    basicRevenue = {}
    deluxRevenue = {}
    totalRevenue = {}
    status = True
    totalRevenue = daysDictionary(openFile('Total.txt'), 1)
    basicRevenue = daysDictionary(openFile('Basic.txt'), 2, 5)
    deluxRevenue = daysDictionary(openFile('Delux.txt'), 2, 6)
    optionDict = {
        "a": [totalRevenue, "Total revenue"],
        "b": [basicRevenue, "Basic cupcakes revenue"],
        "c": [deluxRevenue, "Delux cupcakes revenue"]
    }

    while (status):

        print("[a] [Yearly revenue.]")
        print("[b] [Weekly revenue.]")
        print("[c] [Monthly revenue.]")
        print("[d] [Custom date interval revenue.]")
        print("[e] [Basic cupcakes Revenue vs Delux cupcakes revenue.]")

        print("[x]: Exit")

        option = input("Select option: ")

        if (option == "a"):
            print("You selected: [Yearly revenue.] ")
            optionA = subOption()
            if (optionA != 'x'):
                showGraphYear(optionDict[optionA][0], optionDict[optionA][1])

        elif (option == "b"):
            print("You selected: [Weekly revenue.] ")
            optionB = subOption()
            if (optionB != 'x'):
                showGraphWeekly(optionDict[optionB][0], optionDict[optionB][1])

        elif (option == "c"):
            print("You selected: [Monthly revenue.] ")
            optionC = subOption()
            if (optionC != 'x'):
                showGraphMonthly(optionDict[optionC][0],
                                 optionDict[optionC][1])

        elif (option == "d"):
            print("You selected: [Custom date interval revenue.] ")
            optionD = subOption()
            if (optionD != 'x'):
                showGraphCustom(optionDict[optionD][0])
        elif (option == "e"):
            compareGraph(optionDict["b"][0], optionDict["c"][0])

        else:
            status = False
