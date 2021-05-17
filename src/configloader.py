class ConfigLoader:
    def readFullConfig():
        params = ConfigLoader.readParameters()
        configFile = ConfigLoader.readConfigFile()
        fullConfig = {}
        fullConfig.update(params)
        fullConfig.update(configFile)
        return fullConfig

    def readParameters():
        import sys
        import argparse
        usage_examples = sys.argv[0] + " -db1 /etc/mysql/db1.cnf -db2 /etc/mysql/db2.cnf\n"
        usage_examples += sys.argv[0] + " -db1 /etc/mysql/db1.cnf -s searchvalue -r replacevalue\n"
        parser = argparse.ArgumentParser(epilog=usage_examples,formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-db1",help="Config file path for the database 1", required=True)
        parser.add_argument("-db2", help="Config file path for the database 2")
        parser.add_argument("-s", help="Search string")
        parser.add_argument("-r", help="Replace string")
        parser.add_argument("-o", help="OutputFilePath", default="report.html")
        args = parser.parse_args()
        if args.db2 and (args.s or args.r):
            print("Unicamente puedes comparar o buscar i reemplazar, no puedes utilizar el argumento -db2 i -s o -r al mismo tiempo")
            parser.print_help()
            exit(0)
        config = {}
        config["configfile1"] = args.db1
        config["configfile2"] = args.db2
        config["s"] = args.s
        config["r"] = args.r
        config["filepath"] = args.o
        return config

    def readConfigFile():
        import os
        config = {}
        if os.path.exists(".env"):
            f = open(".env", "r")
            for line in f:
                values = line.split("=")
                config[values[0]] = values[1].split("#")[0]
        return config
