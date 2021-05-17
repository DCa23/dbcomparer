class Comparer:
    def __init__(self, tablesData):
        self.__tablesData = tablesData
        self.__globalCompareReport = ""
        self.__tablesCompareScope = {}

    def globalCompare(self,dbhandler):
        headHtml = """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
    <title>DBComparer</title>
    <style type="text/css">
        body {
            text-align:center;
        }
        .table-sm th, .table-sm td {
            font-size: 12px;
            padding: 0;
        }
        #FirstTable {
            font-size: 40px;
        }
    </style>
  </head><body>"""

        self.__addToGlobalReport(headHtml)
        self.__addToGlobalReport("<h1> Table existence comparison </h1>")
        self.__tablesCompareScope = {}

        AllTables = list(self.__tablesData["db2tables"].keys()) + list(set( list(self.__tablesData["db1tables"].keys())) - set(list(self.__tablesData["db2tables"].keys())))
        TablesToCompare = []

        self.__addToGlobalReport('<table class="table" id="FirstTable"><thead class="thead-dark"> <tr><th scope=\"col\">Table name</th><th scope=\"col\">db1</th><th scope=\"col\">db2</th></tr></thead>')
        for table in AllTables:
            presentInBoth = True
            self.__addToGlobalReport('<tr><td>' + table + '</td>')
            if table not in self.__tablesData["db1tables"].keys():
                self.__addToGlobalReport('<td class="table-danger"><i class="fas fa-times-circle"></i></td>')
                presentInBoth = False
            else:
                self.__addToGlobalReport('<td class="table-success"><i class="fas fa-check-circle"></i></td>')
            if table not in self.__tablesData["db2tables"].keys():
                self.__addToGlobalReport('<td class="table-danger"><i class="fas fa-times-circle"></i></td>')
                presentInBoth = False
            else:
                self.__addToGlobalReport('<td class="table-success"><i class="fas fa-check-circle"></i></td>')
            if presentInBoth:
                TablesToCompare.append(table)
            self.__addToGlobalReport('</tr>')
        self.__addToGlobalReport("</table>")
        self.__addToGlobalReport("<h1> Table comparison: </h1>")
        self.__addToGlobalReport('<input type="text" value="12px" id="fontSize" ><button class="btn btn-primary" type="submit" id="hidebutton" onClick="changeFontSize()" >Change font-size</button>')
        self.__addToGlobalReport('<button class="btn btn-primary" type="submit" id="hidebutton" onClick="hideUnhide()" >Hide equal rows</button>')
        
        
        for table in TablesToCompare:
            self.__addToGlobalReport("<h3> Table: " + table + "</h3>")
            self.__tablesCompareScope[table] = []
            self.__addToGlobalReport("<h4> Column comparison </h4>")
            self.__addToGlobalReport("<ul>")
            for column in self.__tablesData["db1tables"][table]["COLUMNS"]:
                if not column in self.__tablesData["db2tables"][table]["COLUMNS"]:
                    self.__addToGlobalReport("<li>Column: " + column + " present in db1 but not in db2</li>")
                else:
                    if column in self.__tablesData["db2tables"][table]["COLUMNS"]:
                        self.__tablesCompareScope[table].append(column)
                    if not column in self.__tablesData["db1tables"][table]["COLUMNS"]:
                        self.__addToGlobalReport("<li>Column: " + column + " present in db2 but not in db1</li>")
            self.__addToGlobalReport("</ul>")

            self.__addToGlobalReport("<h4> ROW comparison </h4>")
            tableRows = dbhandler.getTableRows(table, self.__tablesCompareScope[table])
            tableReport = self.compareTables(table,tableRows)

            self.__addToGlobalReport('<div class="row"> <div class="col-sm"> ')
            self.__addToGlobalReport('<table class="table table-bordered table-sm"><thead class="thead-dark"> <tr><th  colspan="' + str(len(self.__tablesCompareScope[table])) + '"> DB1: '+ table + ': rows (' + str(self.__tablesData["db1tables"][table]["TOTALROWS"]) + ')</th></tr><tr>')
            for columnName in self.__tablesCompareScope[table]:
                self.__addToGlobalReport('<th>' + columnName + '</th>')
            self.__addToGlobalReport('</tr></thead>')
            for row in tableReport:
                if row[0]:
                    self.__addToGlobalReport('<tr class="bg-success">')
                    for column in row[1]:
                        self.__addToGlobalReport("<td> " + str(column) + "</td>")
                else:
                    self.__addToGlobalReport('<tr class="bg-danger">')
                    for column in row[1]:
                        self.__addToGlobalReport("<td> " + str(column) + "</td>")
                self.__addToGlobalReport("</tr>")
            self.__addToGlobalReport('</table>')
            self.__addToGlobalReport('</div>')

            self.__addToGlobalReport('<div class="col-sm">')
            self.__addToGlobalReport('<table class="table table-bordered table-sm"><thead class="thead-dark"> <tr><th colspan="' + str(len(self.__tablesCompareScope[table])) + '"> DB2: '+ table + ': rows (' + str(self.__tablesData["db2tables"][table]["TOTALROWS"]) + ')</th></tr><tr>')
            for columnName in self.__tablesCompareScope[table]:
                self.__addToGlobalReport('<th>' + columnName + '</th>')
            self.__addToGlobalReport('</tr></thead>')
            for row in tableReport:
                if row[0]:
                    self.__addToGlobalReport('<tr class="bg-success">')
                    for column in row[2]:
                        self.__addToGlobalReport("<td> " + str(column) + "</td>")
                else:
                    self.__addToGlobalReport('<tr class="bg-danger">')
                    for column in row[2]:
                        self.__addToGlobalReport("<td> " + str(column) + "</td>")
                self.__addToGlobalReport("</tr>")
            self.__addToGlobalReport('</table>')
            self.__addToGlobalReport('</div></div>')
        
        htmlCloserAndscripts = """<script>
            hideCommon = false
            function hideUnhide() {
                hideCommon = !hideCommon;
                var equalRows = document.getElementsByClassName("bg-success");
                var hideButton = document.getElementById("hidebutton");
                var i;
                if (hideCommon) {
                    for (i = 0;i < equalRows.length; i++){
                        equalRows[i].hidden = true;
                    }
                    hideButton.innerText = "Unhide equal rows"
                } else {
                    for (i = 0;i < equalRows.length; i++){
                        equalRows[i].hidden = false;
                    }
                    hideButton.innerText = "Hide equal rows"
                }
            }

            function changeFontSize() {
                var TableElements = document.querySelectorAll(".table-sm th,.table-sm td");
                var newFontSize = document.getElementById("fontSize").value;
                var i;
                for (i = 0; i < TableElements.length;i++){
                    TableElements[i].style.fontSize = newFontSize;
                }
            }
            </script>
            </body> </html>
        """
        self.__addToGlobalReport(htmlCloserAndscripts)
        return self.__globalCompareReport

    def __addToGlobalReport(self, txt):
        self.__globalCompareReport = self.__globalCompareReport + txt
        self.__globalCompareReport = self.__globalCompareReport + "\n"

    def compareTables(self, tablename,data):
        row = 0
        report = []
        try:
            for rowDB1 in data["db1"]:
                rowDB2 = data["db2"][row]
                if rowDB1 == rowDB2:
                    report.append([True, rowDB1,rowDB2])
                else:
                    report.append([False,rowDB1,rowDB2])
                row = row + 1
        except Exception as e:
            print("Error comparing database")
            print(str(e))
        finally:
            print("Compared until row: " + str(row))
        return report
