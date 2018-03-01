import MySQLdb

def sendDataToDB():
    conn = MySQLdb.connect(host= "selene.hud.ac.uk",
              user="irobot",
              passwd="IRwy12soas",
              db="irobot")
    x = conn.cursor()

    table_name = "Light"
    values = {"1000"}
    values2 =  {"12:45:12"}
    query = "INSERT INTO " + table_name + "(lightvalues, addedwhen) VALUES (%s, %s)"
    x.execute(query, (values, values2))
    conn.commit()

    conn.close()

def sendValuesToDB(table,coloumnOne,coloumnTwo,value,timeOfValue):
    conn = MySQLdb.connect(host= "selene.hud.ac.uk",
                  user="irobot",
                  passwd="IRwy12soas",
                  db="irobot")
    x = conn.cursor()
    table_name = table
    coloumn_One = coloumnOne
    coloumn_Two = coloumnTwo
    values = value
    timeValue = timeOfValue
    query = "INSERT INTO " + table_name +"("+coloumn_One+", "+coloumn_Two+")"+" VALUES (%s, %s)"
    x.execute(query, (values, timeValue))
    conn.commit()

    conn.close()

sendValuesToDB("Light","lightvalues","addedwhen","30000","12:12:12")



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
