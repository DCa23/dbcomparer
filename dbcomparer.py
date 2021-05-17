#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    from src.dbhandler import DatabaseHandler,DataBaseSR
    from src.comparer import Comparer
    from src.reporter import Reporter
    from src.configloader import ConfigLoader
    from src.slackhandler import SlackHandler
    config = ConfigLoader.readFullConfig()
    if(config["s"]):
        db = DataBaseSR(config["configfile1"])
        tableList = db.getTableList()
        sqlUpdateList = []
        for table in tableList:
            tableName = table[0]
            fullData = db.getFullTable(tableName)
            columnList = db.getColumnsFromTable(tableName)
            for row in fullData:
                columnX = 0
                sqlUp = ""
                sqlWhere = " WHERE "
                for column in row:
                    replaceValue = str(config["r"])
                    searchValue = str(config["s"])
                    columnValue = str(column)
                    if searchValue in columnValue:
                        newValue = columnValue.replace(searchValue,replaceValue)
                        sqlUp += "UPDATE " + tableName 
                        sqlUp += " SET " + columnList[columnX] + "='" + newValue +"' ,"
                    if isinstance(column,str):
                        sqlWhere += columnList[columnX] + "='" + str(column) + "' AND "
                    else:
                        sqlWhere += columnList[columnX] + "=" + str(column) + " AND "
                    columnX = columnX + 1
                if sqlUp:
                    sql = sqlUp[:-1] + sqlWhere[:-4]
                    sqlUpdateList.append(sql)
        db.sqlUpdater(sqlUpdateList)
        exit(0)
    db = DatabaseHandler(config["configfile1"], config["configfile2"])
    tableData = db.getTablesData()
    comparer = Comparer(tableData)
    globalReport = comparer.globalCompare(db)
    reporter = Reporter(config["filepath"])
    reporter.writeReport(globalReport)

    db.closeConnections()
    if "slacktoken" in config and "slackchannel" in config:
        slh = SlackHandler(config["slacktoken"],config["slackchannel"],config["filepath"])
        slh.notifySlack()
    exit(0)

if __name__ == "__main__":
    main()
