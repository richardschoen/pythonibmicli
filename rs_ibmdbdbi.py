# Environment setup
# pip3 install --upgrade ibm-db
#-------------------------------------------------------
# Module: rs_ibmdbdbi.py
# Desc: This module contains our IBM i database class
#       for access IBM i DB2 data via ibm_db_dbi.
#       Note: Currently connections to NOT use committment control. 
#-------------------------------------------------------

#-------------------------------------------------------
# Class: DbIbmDbDbi
# Desc: This class is a wrapper class around IBM i ibm_db_dbi functions
#-------------------------------------------------------
import ibm_db_dbi as db2
from ibm_db_dbi import SQL_ATTR_TXN_ISOLATION, SQL_TXN_NO_COMMIT
import uuid

class DbIbmDbDbi():
 
    # Class variables
    _dbopen=False
    _dbconn=None
    _dbconnstring=""

    def __init__(self,db_connectnow=None):
        #-------------------------------------------------------
        # Function: __init__
        # Desc: Constructor
        # :param self: Object instance
        # :param db_file: File name or default to None if no file 
        #        needs to be opened yet
        # :return: Connection or None on error 
        #-------------------------------------------------------
        try:
           _dbopen=False
           _dbconn=None
           if db_connectnow != None and db_connectnow != False:
              self.create_connection()
           else:
              print("No connection option passed in. Need to create connection later.")
        except Exception as e:
            print(e)
        finally:
            return None #Can return None or omit any return

    def isopen(self):
        #-------------------------------------------------------
        # Function: isopen
        # Desc: Check if database is open 
        # :param self: Pointer to object instance. 
        # :return: True-Db is open, False=Db is not open
        #-------------------------------------------------------
        #return DB open status
        return self._dbopen

    def getconn(self):
        #-------------------------------------------------------
        # Function: getconn
        # Desc: Get database connection object 
        # :param self: Pointer to object instance. 
        # :return: Connection value
        #-------------------------------------------------------
        #return conn object
        return self._dbconn
    
    def create_connection(self):
        #-------------------------------------------------------
        # Function: create_connection
        # Desc: Create a database connection to IBMi database via ibm_db
        # :param self: Pointer to object instance. 
        # :return: True-Connection open, False-No connection open 
        #-------------------------------------------------------

        #Create connection variable
        conn = None 

        #Let's try and open the database. Will auto-create if not found.
        try:
            conn=db2.connect()
            # No commitment control
            conn.set_option({ SQL_ATTR_TXN_ISOLATION: SQL_TXN_NO_COMMIT })
            # Set open flag = true
            if conn != None:
               #Save open connection info internally in the class 
               self._dbopen=True 
               self._dbconn = conn
            return self._dbopen;
        except Exception as e:
            print(e)
            return False

    def close_connection(self):
        #-------------------------------------------------------
        # Function: close_connection
        # Desc: Close a database connection to a db2 database 
        # :param self: Pointer to object instance. 
        # :return: True-Success, False-Error
        #-------------------------------------------------------

        # Let's attempt to close our database connection 
        try:
            self._dbconn.close()
            #Release object. Not sure if needed or automatic ?
            conn=None
            self._dbconn=None
            return True;
        except Exception as e:
            print(e)
            return False

    def execute(self,sql,parameters=None):
        #----------------------------------------------------------
        # Function: execute
        # Desc: Execute an SQL action query that does not return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL action query
        # :return: True-Success, False-Error
        #----------------------------------------------------------
        try:
            cursor1 = self._dbconn.cursor()
            cursor1.execute(sql,parameters)
            return True
        except Exception as e:
            print(e)  
            return False

    def callproc(self,procname,parameters=None):
        #----------------------------------------------------------
        # Function: execute
        # Desc: Execute a stored procedure
        # :param self: Pointer to object instance. 
        # :param sql: SQL action query
        # :return: results or None on error
        #----------------------------------------------------------
        try:
            cursor1 = self._dbconn.cursor()
            result=cursor1.callproc(procname,parameters)
            return result
        except Exception as e:
            print(e)  
            return None

    def execute_query(self,sql):
        #----------------------------------------------------------
        # Function: execute_query
        # Desc: Execute an SQL query that does return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL query expecting results
        # :return: Resulting cursor or None on error
        #----------------------------------------------------------
        try:
            cursor1 = self._dbconn.cursor()
            cursor1.execute(sql)
            return cursor1
        except Exception as e:
            print(e)  
            return None
     
    def getnewguid(self):
        #----------------------------------------------------------
        # Function: getnewguid
        # Desc: Generate new GUID using the uuid1 function
        # :param self: Pointer to object instance. 
        # :return: Resulting guid or None
        #----------------------------------------------------------
        try:
           # generate the guid (uuid1)
           return str(uuid.uuid1())
        except Error as e:
            print(e)  
            return None
