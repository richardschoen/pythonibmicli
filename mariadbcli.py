#!/usr/bin/python
#------------------------------------------------
# Script name: mariadbcli.py
#
# Description: 
# This script will run MySQL/MariaDB database operations
#
# Pip packages needed:
# pip install --upgrade PyMySql (Database driver)
#
# Parameters
# --host - MySQL/MariaDB host (localhost, etc)
# --port - MySQL/MariaDB port (3306, etc)
# --user - MySQL/MariaDB user 
# --password - MySQL/MariaDB password
# --database - MySQL/MariaDB database name
# --action - Action to perform. QUERY - SQL SELECT Query, NONQUERY - SQL non query action. Ex: INSERT, UPDATE, DELETE
# --sql - SQL query or action to run
# --outputtype - Output format for query. csv or json formats
# --delimiter - Output file delimiter for query to csv.
# --outputfile - Output text file for QUERY action. No output for NONQUERY.
# --replace - Replace output file for query. 
#------------------------------------------------

#------------------------------------------------
# Imports
#------------------------------------------------

#https://www.sqlitetutorial.net/sqlite-python/
#https://www.sqlitetutorial.net/sqlite-python/create-tables/
#https://stackabuse.com/python-modules-creating-importing-and-sharing/
#https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
#https://bobbyhadz.com/blog/python-typeerror-object-of-type-decimal-is-not-json-serializable
# Environment setup

import argparse
from distutils.util import * 
import sys
from sys import platform
import os
import time
import traceback
import json
from dbmariadb import DbMariaDb

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
exitcode=0 #Init exitcode
exitmessage=''
parmsexpected=10
reccount=0

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print("MySQL/MariaDB action")
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

#------------------------------------------------
# Define some useful functions
#------------------------------------------------

def str2bool(strval):
    #-------------------------------------------------------
    # Function: str2bool
    # Desc: Constructor
    # :strval: String value for true or false
    # :return: Return True if string value is" yes, true, t or 1
    #-------------------------------------------------------
    return strval.lower() in ("yes", "true", "t", "1")

def trim(strval):
    #-------------------------------------------------------
    # Function: trim
    # Desc: Alternate name for strip
    # :strval: String value to trim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.strip()

def rtrim(strval):
    #-------------------------------------------------------
    # Function: rtrim
    # Desc: Alternate name for rstrip
    # :strval: String value to trim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.rstrip()

def ltrim(strval):
    #-------------------------------------------------------
    # Function: ltrim
    # Desc: Alternate name for lstrip
    # :strval: String value to ltrim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.lstrip()

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic

      # Check to see if all required parms were passed
      ##if len(sys.argv) < parmsexpected + 1:
      ##  raise Exception(str(parmsexpected) + ' required parms - [MariaDB HOST] [MariaDB Port-Int] [MariaDB Database] [MariaDB User] [MariaDB Password]   [Action:QUERY/NONQUERY] [SQL Query] [OutputFile] [Replace-True/False] [Delimiter] [OutputType-CSV/JSON]. Process cancelled.')

      # Set up the command line argument parsing
      # If the parse_args function fails, the program will
      # exit with an error 2. In Python 3.9, there is 
      # an argument to prevent an auto-exit
      parser = argparse.ArgumentParser()
      #parser.add_argument('-o', '--output', action='store_true', 
      #        help="shows output")
      parser.add_argument('--host', required=True,help="MySQL/MariaDB host")
      parser.add_argument('--port', required=True,help="MySQL/MariaDB port")
      parser.add_argument('--user', required=True,help="MySQL/MariaDB user")
      parser.add_argument('--password', required=True,help="MySQL/MariaDB password")
      parser.add_argument('--database', required=True,help="MySQL/MariaDB host")
      parser.add_argument('--outputfile', required=True,help="Query results output file")
      parser.add_argument('--action', default="query", choices=['query','nonquery'],required=False,help="CLI action")
      parser.add_argument('--sql', required=True,help="SQL query")
      parser.add_argument('--delimiter', default=",",required=False,help="Column delimiter")
      parser.add_argument('--replace', default="True",required=False,help="Replace output file. Default value=True")
      parser.add_argument('--outputtype', default="csv", choices=['csv','json'],required=False,help="Output type (CSV,JSON). Default value=CSV")
   
      # Parse the command line arguments 
      args = parser.parse_args()

      
      # Set parameter work variables from command line args
      parmscriptname = sys.argv[0] 
      parmhost = args.host 
      parmport = int(args.port) 
      parmdatabase = args.database 
      parmuser = args.user 
      parmpass = args.password 
      parmaction= args.action 
      parmsqlquery= args.sql
      parmoutputfile = args.outputfile
      parmreplace=str2bool(args.replace)
      parmdelimiter = args.delimiter
      parmoutputtype = args.outputtype      
      print("Python script: " + parmscriptname)
      print(f"Connection info: Host-{parmhost} Port-{parmport} Database-{parmdatabase}")
      print("SQL action: " + parmaction)
      print("SQL: " + parmsqlquery)
      print("Output file: " + parmoutputfile)
      print("Replace: " + str(parmreplace))
      print("Field delimiter: " + parmdelimiter)      
      filealreadyexists=False

      # Instantiate db class and open or create database
      db=DbMariaDb(parmhost,parmuser,parmpass,parmdatabase,parmport)

      # Run select query or action query
      if parmaction.lower() == 'query':

         # Make sure query starts with SELECT
         if parmsqlquery.lower().startswith('select')==False: 
            raise Exception('SQL query action of:' + str(parmsqlquery) + ' must start with SELECT for QUERY action.')   

         # Replace file
         filealreadyexists=False  
         if os.path.isfile(parmoutputfile):
           if parmreplace==True:
              os.remove(parmoutputfile)
              print("Existing file " + parmoutputfile + " deleted before processing.")
           else:
              # File exists so we will be appending. Skip header 
              filealreadyexists=True  
              print("Existing file " + parmoutputfile + " will be appended to.")
 
         # Run the query now
         print("About to run query")
         c1=db.execute_query(parmsqlquery)
      
         # Open the output file
         f = open(parmoutputfile,"a+")

         # Output as CSV format
         if parmoutputtype.lower() == 'csv': 

            # If we got data results, fetch and display records   
            if c1 == None:
               raise Exception('SQL query action of:' + str(parmsqlquery) + ' failed.')   
   
            if c1 != None:
              rows = c1.fetchall()

              # Get field metadata names from cursor
              column_names = [desc[0] for desc in c1.description]
              rowheader=""
              tempdelim=""
              # Iterate and output column names
              for colname in column_names:
                  # Append value to consolidated row header record
                  rowheader = rowheader + str(colname) + parmdelimiter
              # Output row header only for new file. Skip last char 
              # to remove trailing delimiter on the last field
              if filealreadyexists==False:
                 f.write(rowheader[0:len(rowheader)-1] + "\r\n")
   
              # Iterate and output data rows 
              reccount=0
              for row in rows:
                 rowdata=""
                 # Iterate all columns in each row
                 for col in row:
                     # Append value to consolidated row data record
                     rowdata = rowdata + str(row[col]) + parmdelimiter
                 # Output data row and increment record count Skip last char 
                 # to remove trailing delimiter on the last field
                 f.write(rowdata[0:len(rowdata)-1] + "\r\n")
                 reccount += 1

              # Output row count
              print(str(reccount) + " rows written to CSV/delimited output file " + parmoutputfile)

          # Output as JSON format
         if parmoutputtype.lower() == 'json':
          
            # If we got data results, fetch and display records   
            if c1 == None:
               raise Exception('SQL query action of:' + str(parmsqlquery) + ' failed.')   
   
            if c1 != None:
              rows = c1.fetchall()

              # Get field metadata names from cursor
              column_names = [desc[0] for desc in c1.description]
   
              # Iterate and output data rows to array 
              reccount=0
              json_data=[]
              for row in rows:
                 ##json_data.append(dict(zip(column_names,row)))
                 json_data.append(row)
                 reccount += 1

              # Format data as JSON and write to file
              #f.write("{\"records\":")
              ##print(json_data) 
              f.write("{\"records\":" + f"{json.dumps(json_data,default=str)}" + "}") ## THis ex adds a json: array header
              #f.write("}")
              #f.write(f"json: {json.dumps(json_data)}") ## THis ex adds a json: array header
              #f.write(f"{json.dumps(json_data)}") #Just dump the JSON array
                 
              # Output row count
              print(str(reccount) + " rows written to JSON output file " + parmoutputfile)
   
         # Close the file 
         f.close()

      elif parmaction.lower() == 'nonquery':
      
         # Remove output file if found and replace selected. 
         filealreadyexists=False  
         if os.path.isfile(parmoutputfile):
           if parmreplace==True:
              os.remove(parmoutputfile)
              print("Existing file " + parmoutputfile + " deleted before processing.")
           else:
              # File exists so we will be appending. Skip header 
              filealreadyexists=True  
              print("Existing file " + parmoutputfile + " will be appended to.")

         # Run action query       
         rtnaction=db.execute(parmsqlquery)
         
         # If errors, bail out
         if (rtnaction != True): 
             raise Exception('SQL nonquery action of:' + str(parmsqlquery) + ' failed.')   
  
      else:
         raise Exception('Invalid action of:' + str(parmaction) + ' was selected for action.')   
  
      # Close connection
      if db.isopen():
        db.close_connection()

      # Set success info
      exitcode=0
      exitmessage='Completed successfully'

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
except Exception as ex: # Catch and handle exceptions
   exitcode=99 # set return code for stdout
   exitmessage=str(ex) # set exit message for stdout
   print('Traceback Info') # output traceback info for stdout
   traceback.print_exc()        

#------------------------------------------------
# Always perform final processing
#------------------------------------------------
finally: # Final processing
    # Do any final code and exit now
    # We log as much relevent info to STDOUT as needed
    print('RecordCount:' + str(reccount))
    print('ExitCode:' + str(exitcode))
    print('ExitMessage:' + exitmessage)
    print("End of Main Processing - " + time.strftime("%H:%M:%S"))
    print("-------------------------------------------------------------------------------")
    
    # Exit the script now
    sys.exit(exitcode) 
