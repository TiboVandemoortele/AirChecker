class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "Air-checker",
            "passwd": "root",
            "db": "AirChecker"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    # CO2 sensor
    def listCO2table(self):

        sqlQuery = "SELECT co2.Date,co2.Time,co2.Waarde_ppm,co2.Stijging_daling_ppm, relatieve_kwaliteit.kwaliteit FROM co2 INNER JOIN relatieve_kwaliteit ON co2.relatieve_kwaliteit_ID = relatieve_kwaliteit.ID ORDER BY Date, Time DESC LIMIT 20;"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def listCO2graf(self):
        sqlQuery = "SELECT Date,Time,Waarde_ppm FROM co2 ORDER BY Date,Time DESC LIMIT 10"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def huidigeWaardeCo2(self):
        q = "SELECT co2.Waarde_ppm,co2.Stijging_daling_ppm, relatieve_kwaliteit.kwaliteit FROM co2 INNER JOIN relatieve_kwaliteit ON co2.relatieve_kwaliteit_ID = relatieve_kwaliteit.ID ORDER BY Date, Time DESC LIMIT 1;"
        self.__cursor.execute(q)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result


    # CO sensor
    def listCOtable(self):

        sqlQuery = "SELECT co.Date,co.Time,co.CO_aanwezig, relatieve_kwaliteit.kwaliteit FROM co INNER JOIN relatieve_kwaliteit ON co.relatieve_kwaliteit_ID = relatieve_kwaliteit.ID ORDER BY Date, Time DESC LIMIT 20;"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def listCOgraf(self):
        sqlQuery = "SELECT Date,Time,Relatieve_kwaliteit_ID FROM co ORDER BY Date,Time DESC LIMIT 10"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def huidigeWaardeCo(self):
        q = "SELECT co.CO_aanwezig, relatieve_kwaliteit.kwaliteit FROM co INNER JOIN relatieve_kwaliteit ON co.relatieve_kwaliteit_ID = relatieve_kwaliteit.ID ORDER BY Date, Time DESC LIMIT 1;"
        self.__cursor.execute(q)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result


    # luchtvochtigheid
    def listluchtvochttable(self):
        sqlQuery = "SELECT luchtvochtigheid.Date,luchtvochtigheid.Time,luchtvochtigheid.Waarde_procent,luchtvochtigheid.Stijging_daling_procent, relatieve_kwaliteit.kwaliteit FROM luchtvochtigheid INNER JOIN relatieve_kwaliteit ON luchtvochtigheid.Relatieve_kwaliteit_ID = relatieve_kwaliteit.ID ORDER BY Date, Time DESC LIMIT 20;"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def listluchtvochtgraf(self):
        sqlQuery = "SELECT Date,Time,Waarde_procent FROM luchtvochtigheid ORDER BY Date,Time DESC LIMIT 10"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def huidigeWaardeluchtvocht(self):
        q = "SELECT luchtvochtigheid.Waarde_procent,luchtvochtigheid.Stijging_daling_procent, relatieve_kwaliteit.kwaliteit FROM luchtvochtigheid INNER JOIN relatieve_kwaliteit ON luchtvochtigheid.Relatieve_kwaliteit_ID = relatieve_kwaliteit.ID ORDER BY Date, Time DESC LIMIT 1;"
        self.__cursor.execute(q)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    # temp sensor

    def listtemptable(self):
        sqlQuery = "SELECT Date,Time,Waarde_celcius,Stijging_daling_C,waarde_fahrenheit,stijging_daling_fahrenheit FROM temperatuur ORDER BY Date,Time DESC LIMIT 20"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def listtempgraf(self):
        sqlQuery = "SELECT Date,Time,Waarde_celcius,waarde_fahrenheit FROM temperatuur ORDER BY Date,Time DESC LIMIT 10"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__connection.close()
        return result

    def huidigeWaardetemp(self):
        q = "SELECT Waarde_celcius,Stijging_daling_C,waarde_fahrenheit,stijging_daling_fahrenheit FROM temperatuur ORDER BY Date,Time DESC LIMIT 1"
        self.__cursor.execute(q)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

        # settings

    def update_minuten(self, minuten):
        q = "UPDATE time_between SET minuten = " + minuten + "WHERE ID = 1"
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()

    def update_relay(self, state):
        q = "UPDATE relay SET state = " + state + "WHERE relay = '230V_ALWAYS'"
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()

    def update_safety(self, state):
        q = "UPDATE relay SET state = " + state + "WHERE relay = '230V_GAS'"
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()

    def update_motor(self, state):
        q = "UPDATE relay SET state = " + state + "WHERE relay = 'Motor'"
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()