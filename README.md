# IBM i Python CLI Scripts to query databases or insert, update delete individual records
This repository will contain ready-to-run command line (CLI) utility app examples for querying and updating data using a command line Python script.   

Sample CL wrappers will also be added that call the scripts via an IBM i CL command.     

Several versions will be added for: IBM i DB2, SQLite, MariaDB, PostgreSQL and SQL Server. Possibly more.

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




