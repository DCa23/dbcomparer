class Reporter:

    def __init__(self, filepath):
        self.__filepath = filepath
        self.openFiles()

    def writeReport(self, text):
        try:
            self.__file.write(text)
        except Exception as e:
            print("Error writing the report")
            print(str(e))

    def closeFiles(self):
        try:
            self.__file.close()
        except Exception as e:
            print("Error closing the report")
            print(str(e))

    def openFiles(self):
        try:
            self.__file = open(self.__filepath, "w")
        except Exception as e:
            print("Error opening the report")
            print(str(e))

    def reopenFiles(self):
        self.closeFiles()
        self.openFiles()
