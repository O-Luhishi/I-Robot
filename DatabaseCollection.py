import MySQLdb

class DataCollection():
    def __init__(self):
            pass

    def connectToDB(self):
        global conn, x
        conn = MySQLdb.connect(host= "selene.hud.ac.uk",
                  user="irobot",
                  passwd="IRwy12soas",
                  db="irobot")
        x = conn.cursor()

    def sendValuesToDB(self,table,coloumnOne,coloumnTwo,value,timeOfValue):
        self.connectToDB()
        try:
            table_name = table
            coloumn_One = coloumnOne
            coloumn_Two = coloumnTwo
            values = value
            timeValue = timeOfValue
            query = "INSERT INTO " + table_name +"("+coloumn_One+", "+coloumn_Two+")"+" VALUES (%s, %s)"
            x.execute(query, (values, timeValue))
            conn.commit()
            print 'done'
        except:
            print 'not done'
            conn.rollback()

        conn.close()
