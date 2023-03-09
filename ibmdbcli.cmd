             CMD        PROMPT('Native ibm_db CLI Cmd Wrapper')
             PARM       KWD(SCRIPTFILE) TYPE(*CHAR) LEN(255) +
                          RSTD(*NO) MIN(1) MAX(1) CASE(*MIXED) +
                          PROMPT('Python script file')
             PARM       KWD(SQL) TYPE(*CHAR) LEN(4000) MIN(1) MAX(1) +
                          CASE(*MIXED) PROMPT('SQL query or action +
                          execute')
             PARM       KWD(ACTION) TYPE(*CHAR) LEN(50) RSTD(*NO) +
                          DFT('QUERY') SPCVAL((QUERY 'query') +
                          (NONQUERY 'nonquery')) MAX(1) CASE(*MIXED) +
                          PROMPT('Action')
             PARM       KWD(OUTPUTFILE) TYPE(*CHAR) LEN(255) +
                          RSTD(*NO) MAX(1) CASE(*MIXED) +
                          PROMPT('Output file for queries')
             PARM       KWD(REPLACE) TYPE(*CHAR) LEN(5) RSTD(*YES) +
                          DFT(*YES) VALUES(*NO *YES) SPCVAL((*NO +
                          'False') (*YES 'True')) MAX(1) +
                          CASE(*MIXED) PROMPT('Replace output file')
             PARM       KWD(FIELEDELIM) TYPE(*CHAR) LEN(2) RSTD(*NO) +
                          DFT('|') MAX(1) CASE(*MIXED) +
                          PROMPT('Field delimiter')
             PARM       KWD(OUTPUTTYPE) TYPE(*CHAR) LEN(10) +
                          RSTD(*YES) DFT(CSV) VALUES(JSON CSV) +
                          SPCVAL((JSON 'json') (CSV 'csv')) MAX(1) +
                          CASE(*MIXED) PROMPT('Output type')
             PARM       KWD(VIEWOUTPUT) TYPE(*CHAR) LEN(5) +
                          RSTD(*YES) DFT(*NO) VALUES(*NO *YES) +
                          MAX(1) CASE(*MIXED) PROMPT('View output +
                          file')
             PARM       KWD(PROMPT) TYPE(*CHAR) LEN(4) RSTD(*YES) +
                          DFT(*NO) VALUES(*NO *YES) MAX(1) +
                          CASE(*MIXED) PROMPT('Show QSHEXEC prompt')
             PARM       KWD(DSPSTDOUT) TYPE(*CHAR) LEN(4) RSTD(*YES) +
                          DFT(*NO) VALUES(*NO *YES) PROMPT('Display +
                          standard output result')
             PARM       KWD(LOGSTDOUT) TYPE(*CHAR) LEN(4) RSTD(*YES) +
                          DFT(*NO) VALUES(*NO *YES) PROMPT('Log +
                          standard output to job log')
             PARM       KWD(PRTSTDOUT) TYPE(*CHAR) LEN(4) RSTD(*YES) +
                          DFT(*NO) VALUES(*NO *YES) PROMPT('Print +
                          standard output result')
             PARM       KWD(DLTSTDOUT) TYPE(*CHAR) LEN(4) RSTD(*YES) +
                          DFT(*YES) VALUES(*NO *YES) PROMPT('Delete +
                          standard output result')
 QUAL2:      QUAL       TYPE(*NAME) LEN(10) DFT(SQLSTDOUT) EXPR(*YES)
             QUAL       TYPE(*NAME) LEN(10) DFT(QTEMP) EXPR(*YES) +
                          PROMPT('Library')
