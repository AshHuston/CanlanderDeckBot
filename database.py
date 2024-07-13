import json
import os
import secrets
# import cryptography
import random
import ast

encrytionCharacters = [' ', '"', '\'', ':', ';', '<', '>', '/', '-', '+', '=', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '?', '~', '`', '_', '[', ']', '|', '.', ',', '{', '}', 
                      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                      '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

class database:
    """This class creates and stores a simple database to be accessed by the application.

    Args:
        dbName (str): The name of the database and the file it is stored in. "db_" will be appended to the front.
        columns (list): A list of strings containing the names of the columns.

    """

    dbName = ""
    columnNames = []
    filename = ""
    encryptionKey = ""
    
    def generateEncryptionKey(self):
        global encrytionCharacters
        characters = encrytionCharacters
        key = ""
        random.shuffle(characters)
        for i in range(len(characters)):
            key += characters[i]
        return key
       
    def encrypt(self, key, plainMessage):
        return plainMessage #--------------------# This is literally just to pypass the function bc we can't store the key.
        global encrytionCharacters
        characters = encrytionCharacters
        #plainMessage = plainMessage.lower()
        encodedMessage = ""
        length = range(len(plainMessage))
        for i in length:
            newChar = "\n"
            if plainMessage[i] != "\n":
                for n in range(len(characters)):
                    if plainMessage[i] == characters[n]:
                        newCharIndex = i+n #
                while newCharIndex >= len(key):
                    newCharIndex -= len(key)
                newChar = key[newCharIndex]
            encodedMessage += newChar
        return encodedMessage

    def decrypt(self, key, encodedMessage):
        return encodedMessage #--------------------# This is literally just to pypass the function bc we can't store the key.
        global encrytionCharacters
        characters = encrytionCharacters
        plainMessage = ""
        length = range(len(encodedMessage))
        for i in length:
            newChar = "\n"
            if encodedMessage[i] != "\n":
                for n in range(len(key)):
                    if encodedMessage[i] == key[n]:
                        originalCharIndex = n-i #
                while originalCharIndex < 0:
                    originalCharIndex += len(characters)
                newChar = characters[originalCharIndex]
            plainMessage += newChar
        return plainMessage

    def getLines(self):
        file = open(self.filename, 'r')
        text = file.read()
        file.close()
        decryptedText = self.decrypt(self.encryptionKey, text)
        return decryptedText.split("\n")

    def setLines(self, lines):
        try:
            file = open(self.filename, 'w')            
            for each in lines:
                encryptedText = self.encrypt(self.encryptionKey, each)
                if each == lines[0]:
                    file.write(encryptedText)
                else:
                    file.write('\n' + encryptedText)

            file.close()
            return True
        except:
            return False

    def __init__(self, dbName, valueKeys):
        self.encryptionKey = "8d}%yRw]a!X@OU/LESnpVcMNf1s9AgP)rTuo>iIKH[h,$kGzQ:7 =j\";WDm43&YCB?2e{+b#(l_5'`<~F|-Jxtvq*0.6Z^"
        # = self.generateEncryptionKey()
        self.filename = "db_"+dbName+".txt"
        filePath = self.filename
        self.dbName = dbName

        if not os.path.isfile(filePath):
            file = open(self.filename, 'w')
            firstLine = "| "
            for keys in valueKeys:
                firstLine += (keys+" | ")
            file.write(firstLine)
            file.close()
            self.columnNames = valueKeys
            self.columnNames.append('row')
        else:
            self.columnNames = self.getLines()[0].split("|")
            for i in range(len(self.columnNames)):
                self.columnNames[i] = self.columnNames[i].strip()

    def addRowNums(self):
        allRows = self.getLines()
        for i in range(len(allRows)):
            if i>0:
                dict = ast.literal_eval(allRows[i])
                jsonString = json.dumps(dict)
                dbEntry = json.loads(jsonString)
                dbEntry['row'] = i
                allRows[i] = str(dbEntry)
        self.setLines(allRows)

    def addRow(self, dataDictionary):
        """Adds a new row of data to the database.

        Args:
            dataDictionary (dict): The data to be added as a row.
        """
        for each in dataDictionary:
            if each not in self.columnNames:
                raise Exception("ERROR: '" + each + "' is not a valid column for database '" + self.dbName + "'.")

        file = open(self.filename, 'a')
        file.write("\n"+str(dataDictionary))
        file.close()
        self.addRowNums()

    def deleteRow(self, row):
        """Delete the row numbered 'row' from the database.

        Args:
            row (int): The row to remove from the database.
        """
        lines = self.getLines
        if len(lines)<row:
            raise Exception("ERROR: '" + row + "' out of range for database '" + self.dbName + "'.")
        file = open(self.filename, 'w')
        for i in range(len(lines)):
            if i != row:
                lines.pop(i)
        file.writelines(lines)   

    def updateValue(self, row, key, value):
        """Updates a specified value in a given row.

        Args:
            row (int): Row to find value in.
            key (str): Key of the value to update.
            value (any): New value.

        Raises:
            Exception: Row is out of range.
            Exception: Key not found.

        Returns:
            bool: True if value gets updated. False otherwise.
        """
        lines = self.getLines()
        if len(lines)<row:
            raise Exception("ERROR: '" + row + "' out of range for database '" + self.dbName + "'.")
        dbEntry = json.loads(lines[row].replace("\'", "\""))
        if key in self.columnNames:
            try:
                dbEntry[key] = {value}
                lines[row] = str(dbEntry)
                self.setLines(lines)
                self.addRowNums()
                return True
            except:
                return False
        else:
            raise Exception("ERROR: '" + key + "' is not a valid key for database '" + self.dbName + "'.")

    def updateRow(self, row, data):
        """Updates the full row to match data. Will throw and exception if data does not fit the columns.
        Any missing values will be given the value of "---".

        Args:
            row (int): The row to be replaced.
            data (str): The data to replace the row.

        Raises:
            Exception: Row is out of range.
            Exception: Key not found.
        """
        lines = self.getLines()
        if len(lines)<row:
            raise Exception("ERROR: '" + row + "' out of range for database '" + self.dbName + "'.")
        dict = ast.literal_eval(data)
        jsonString = json.dumps(dict)
        jsonData = json.loads(jsonString)
        varsAdded = []
        for each in jsonData:
            varsAdded.append(each)
            if each not in self.columnNames:
                raise Exception("ERROR: '" + each + "' is not a valid key for database '" + self.dbName + "'.")
        for cols in self.columnNames:
            if cols not in varsAdded and cols != "":
                jsonData[cols] = "---"
        lines = self.getLines()
        lines[row] = str(jsonData)
        self.setLines(lines)
        self.addRowNums()

    def getValue(self, row, key):
        """Returns the value of a specified key in a given row.

        Args:
            row (int): The row to find the value in.
            key (str): The key of the value.

        Returns:
            any: The value of the searched row/key.
        """
        lines = self.getLines()
        try:
            dict = ast.literal_eval(lines[int(row)])
        except:
            print(f"Row {row} does not exist.")
            raise Exception
        jsonString = json.dumps(dict)
        dbEntry = json.loads(jsonString)
        value = dbEntry[key]
        return value
    
    def getRows(self, key, value, caseSensitive=False):
        """Returns the row(s) that have a specific value at a given key.

        Args:
            key (str): The key to check for
            value (any): The value to check for in the key.

        Returns:
            str or str[]: Returns either the matching row, or a list of them if multiple matches are found. Empty list if no matches.
        """
        foundRows = []
        lines = self.getLines()
        for rows in lines:
            try:
                dict = ast.literal_eval(rows)
                jsonString = json.dumps(dict)
                rowJson = json.loads(jsonString)
            except:
                if rows == lines[0]:
                    continue
                else:
                #    print('Failed to convert to json')
                    continue
            match caseSensitive:
                case True:
                    if rowJson[key] == value:
                        foundRows.append(rowJson)
                case False:
                    if str(rowJson[key]).lower() == str(value).lower():
                        foundRows.append(rowJson)
        if len(foundRows) == 1:
            return foundRows[0]
        else:
            return foundRows
        
    def getValuesFromRows(self, returnKey, targetKey, value):
        """Returns an array(or just the value if singular) from the rows where the target

        Args:
            returnKey (str): They key to return from matching lines.
            targetKey (str): The key to look for matches with.
            value (any): The value to match the targetKey to.

        Returns:
            any: Returns either the appropriate value of the matching row, or a list of them if multiple matches are found.
        """
        foundVals = []
        lines = self.getLines()
        for rows in lines:
            try:
                rowJson = json.loads(rows.replace("\'", "\""))
            except:
               # print('failed to convert to json')
                continue
            if rowJson[targetKey] == value:
                foundVals.append(rowJson[returnKey])
        if len(foundVals) == 1:
            return foundVals[0]
        else:
            return foundVals

    def getRowNumbers(self, targetKey, valueAny, fuzzy=False, caseSensitive=False): #Maybe should rework this to allow conditions, not just matching...
        """Returns an array(or just the value if singular) from the rows that match.

        Args:
            targetKey (str): The key to look for matches with.
            value (any): The value to match the targetKey to.

        Returns:
            any: Returns either the row number of the matching row, or a list of them if multiple matches are found.
        """
        value = str(valueAny)
        foundRowNumbers = []
        lines = self.getLines()
        for rows in lines:
            try:
                dict = ast.literal_eval(rows)
                jsonString = json.dumps(dict)
                rowJson = json.loads(jsonString)
            except:
                continue

            match caseSensitive:
                case True:
                    if fuzzy:
                        if rowJson[targetKey].count(value) > 0:
                            foundRowNumbers.append(rowJson['row'])
                    else:
                        if rowJson[targetKey] == value:
                            foundRowNumbers.append(rowJson['row'])
                case False:
                    if fuzzy:
                        if str(rowJson[targetKey]).lower().count(value.lower()) > 0:
                            foundRowNumbers.append(rowJson['row'])
                    else:
                        if str(rowJson[targetKey]).lower() == value.lower():
                            foundRowNumbers.append(rowJson['row'])

        if len(foundRowNumbers) == 1:
            return foundRowNumbers[0]
        else:
            return foundRowNumbers

    # These two functions, addColumn() and deleteColumn(), should maybe add/remove the properties from the lines. As of now they don't, obviously.
    def addColumn(self, newColumnName):
        """Adds a new column to the database.

        Args:
            newColumnName (str): The key to refer to the column.

        Raises:
            Exception: Any failure.
        """
        try:
            self.columnNames.append(newColumnName)
        except:
            raise Exception("Failed to add new column to database '" + self.dbName + "'.")
        
    def deleteColumn(self, columnName):
        """Removes a column from the database.

        Args:
            columnName (str): The key to refer to the column.

        Raises:
            Exception: Any failure.
        """
        try:
            self.columnNames.remove(columnName)
        except:
            raise Exception("Failed to remove column from database '" + self.dbName + "'.")