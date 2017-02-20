class DBManager():
    count=0
    def setDBName(self,dbname):
        self.DBName=dbname

    def setTableName(self,tablename):
        self.tableName=tablename

    def setHost(self,host):
        self.host=host

    def setPort(self,port):
        self.port=port

    def getCount(self):
        return self.count

    def incrementCount(self):
        self.count += 1

    def connect(self):
        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[self.DBName]
        self.collection = self.db[self.tableName]

    def insertOne(self,element):
        self.collection.insert_one(element)
        self.incrementCount()

    def find(self,filters=None):
        if( filters==None):
            databaseContent = self.collection.find()
        else:
            databaseContent = self.collection.find(filters)
        return databaseContent
