class DatabaseHandler:

    def __init__(self, dbfile1, dbfile2):
        try:
            import mysql.connector
            self.__dbfile1 = dbfile1
            self.__dbfile2 = dbfile2
            self.__dbconnection1 = mysql.connector.connect(
                option_files=dbfile1)
            self.__dbconnection2 = mysql.connector.connect(
                option_files=dbfile2)
        except Exception as e:
            print("Error connecting to database")
            print(str(e))
            exit(1)

    def closeConnections(self):
        try:
            self.__dbconnection1.close()
            self.__dbconnection2.close()
        except Exception as e:
            print("Error closing database connections")
            print(str(e))

    def startConnections(self):
        try:
            import mysql.connector
            self.__dbconnection1 = mysql.connector.connect(
                option_files=self.__dbfile1)
            self.__dbconnection2 = mysql.connector.connect(
                option_files=self.__dbfile2)
        except Exception as e:
            print("Error connecting to database")
            print(str(e))
            exit(1)

    def restartConnections(self):
        self.closeConnections()
        self.startConnections()

    def __queryArray(self, dbconnection, sql):
        cursor = dbconnection.cursor()
        cursor.execute(sql)
        rawresult = cursor.fetchall()
        return rawresult

    def getTablesData(self):
        tableSql = "SHOW TABLES"
        tables = self.__queryArray(self.__dbconnection1, tableSql)
        tablesData = {
            "db1tables": {},
            "db2tables": {},
        }
        for table in tables:
            tablename = table[0]
            tablesData["db1tables"][tablename] = {}
            sql = "SELECT count(*) as TOTAL FROM " + tablename
            totalrows = self.__queryArray(self.__dbconnection1, sql)
            tablesData["db1tables"][tablename]["TOTALROWS"] = totalrows[0][0]
            tablesData["db1tables"][tablename]["COLUMNS"] = []
            sql = "SHOW COLUMNS FROM " + tablename
            columns = self.__queryArray(self.__dbconnection1, sql)
            for column in columns:
                tablesData["db1tables"][tablename]["COLUMNS"].append(column[0])

        tables = self.__queryArray(self.__dbconnection2, tableSql)
        for table in tables:
            tablename = table[0]
            tablesData["db2tables"][tablename] = {}
            sql = "SELECT count(*) as TOTAL FROM " + tablename
            totalrows = self.__queryArray(self.__dbconnection2, sql)
            tablesData["db2tables"][tablename]["TOTALROWS"] = totalrows[0][0]
            tablesData["db2tables"][tablename]["COLUMNS"] = []
            sql = "SHOW COLUMNS FROM " + tablename
            columns = self.__queryArray(self.__dbconnection2, sql)
            for column in columns:
                tablesData["db2tables"][tablename]["COLUMNS"].append(column[0])
        return tablesData

    def getTableRows(self, table, columns):
        sql = "SELECT "
        for column in columns:
            sql = sql + column + ","
        sql = sql[:-1] + " FROM " + table
        sql = sql + " ORDER BY " + columns[0]
        data = {}
        data["db1"] = self.__queryArray(self.__dbconnection1, sql)
        data["db2"] = self.__queryArray(self.__dbconnection2, sql)
        return data


class DataBaseSR:

    def __init__(self, dbfile1):
        try:
            import mysql.connector
            self.__dbfile1 = dbfile1
            self.__dbconnection1 = mysql.connector.connect(option_files=dbfile1)
        except Exception as e:
            print("Error connecting to database")
            print(str(e))
            exit(1)

    def closeConnections(self):
        try:
            self.__dbconnection1.close()
        except Exception as e:
            print("Error closing database connections")
            print(str(e))

    def startConnections(self):
        try:
            import mysql.connector
            self.__dbconnection1 = mysql.connector.connect(
                option_files=self.__dbfile1)
        except Exception as e:
            print("Error connecting to database")
            print(str(e))
            exit(1)

    def restartConnections(self):
        self.closeConnections()
        self.startConnections()

    def __queryArray(self, dbconnection, sql):
        try:
            cursor = dbconnection.cursor()
            cursor.execute(sql)
            rawresult = cursor.fetchall()
            return rawresult
        except Exception as e:
            print("Error executing the query\n" + str(e))

    def __execSql(self, dbconnection, sql):
        try:
            cursor = dbconnection.cursor()
            cursor.execute(sql)
            dbconnection.commit()
        except Exception as e:
            print("Error executing the query\n" + str(e))


    def getTableList(self):
        try:
            tableSql = "SHOW TABLES"
            tables = self.__queryArray(self.__dbconnection1, tableSql)
            return tables
        except Exception as e:
            print("Error executing the query\n" + str(e))

    def getColumnsFromTable(self,table):
        try:
            colList = []
            colSql = "SHOW COLUMNS FROM " + table
            columns = self.__queryArray(self.__dbconnection1,colSql)
            for column in columns:
                colList.append(column[0])
            return colList
        except Exception as e:
            print("Error executing the query\n" + str(e))

    def getFullTable(self,table):
        try:
            sql = "SELECT * FROM " + table
            fulldata = self.__queryArray(self.__dbconnection1,sql)
            return fulldata
        except Exception as e:
            print("Error executing the query\n" + str(e))
    
    def sqlUpdater(self,sqlList):
        try:
            for sql in sqlList:
                self.__execSql(self.__dbconnection1,sql)
        except Exception as e:
            print("Error executing the query\n" + str(e))