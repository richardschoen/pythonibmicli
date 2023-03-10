# IBM i Python CLI Scripts to query databases or insert, update delete individual records
This repository will contain ready-to-run command line (CLI) utility app examples for querying, inserting and updating data using a command line Python script.   

Sample CL wrappers will also be added that call the scripts via an IBM i CL command.     

```Several versions will be added for: IBM i DB2, ODBC, SQLite, MariaDB, PostgreSQL and SQL Server. Possibly more.```

# Use Case
RPG and CL cannot easily directly communicate with remote databases.   

These Python scripts and commands will provide an easy way to query remote data and bring back results as ```CSV or other delimited resultsets``` for consumption directly from the IFS by an RPG program or by importing to a database via the ```CPYFRMIMP``` command (Copy From Import File).   

Record results can also be returned in ```JSON``` format. These results can be then consumed in RPG via the ```YAJL``` library ported by Scott Klement (https://www.scottklement.com/yajl), ```noxDB``` library (https://github.com/sitemule/noxDB) or the ```DATA-INTO``` opcode in RPG (https://www.ibm.com/docs/en/i/7.5?topic=codes-data-into-parse-document-into-variable).   

INSERT, UPDATE and DELETE commands can also be issued to update the selected remote database as well covering the entire CRUD cycle for data access. 

# ibmdbcli.py - Python command line interface (CLI) script to query or write data to DB2 with ibm_db driver
This script will run IBM DB2 database operations via native DB2 driver: python-ibmdb.

This script is similar to the IBM i ```db2util``` pase app for querying data, but it's a native Python scripting.

**IBM i prerequisites**   
IBM i V7R3 and above   
Python 3.6 or 3.9 on IBM i   
QShell on i - (http://www.github.com/richardschoen/qshoni)  

**Pip packages needed**  
```pip install ibm_db``` (IBM Database driver)  
  
**Parameters**
```
--action - Action to perform. 
           QUERY - SQL SELECT Query     
           NONQUERY - SQL non query action. Ex: INSERT, UPDATE, DELETE  
           **NOTE: The CLI will not currently work with stored procedures.  
--sql - SQL query or action to run  
--outputtype - Output format for query. csv or json formats  
--delimiter - Output file delimiter for query to csv. Default = ,  
--outputfile - Output text file for QUERY action. No output for NONQUERY.  
--replace - Replace output file for query. True/False. Default = True  
```

**Examples**

Query table QIWS/QCUSCTDT and write to IFS file as CSV
```python3 ibmdbcli.py --sql "select * from qiws.qcustcdt" --outputfile "/tmp/qcustcdt.csv" --replace "true" --outputtype "csv" --delimiter ","```  

Query table QIWS/QCUSCTDT and write to IFS file as JSON
```python3 ibmdbcli.py --sql "select * from qiws.qcustcdt" --outputfile "/tmp/qcustcdt.csv" --replace "true" --outputtype "json"```  

Insert new record into table QIWS/QCUSTCDT
```python3 ibmdbdb.py --sql "insert into qiws.qcustcdt (cusnum,lstnam) values(123456,'Jones') " --outputfile "/tmp/qcustcdt.txt" --action "nonquery"```

# IBMDBCLI - CL wrapper command front end for ibmdbcli.py

Query table QIWS/QCUSCTDT and write to IFS file as CSV file.   
Calls the ibmdbcli.py Python script via the QSHONI/QSHEXEC command. 

```
IBMDBCLI SCRIPTFILE('/pythonapps/ibmdbcli.py')                                      
         SQL('select * from qiws.qcustcdt')                  
         ACTION('QUERY')                                     
         OUTPUTFILE('/tmp/qcustcdt.csv')                          
         FIELEDELIM(',')                                     
         REPLACE(*YES) 
         OUTPUTTYPE(CSV)
```
