class DataBase:
    def _log(self,str):
        print("DataBase:"+str);
    def __init__(self):
        self._log("---init---")

if __name__ == "__main__":
    dataBase = DataBase()
