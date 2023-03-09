             PGM        PARM(&SCRIPTFILE &SQL &ACTION &OUTPUTFILE +
                          &REPLACE &FIELDDELIM &OUTPUTTYPE +
                          &VIEWOUTPUT &PROMPT &DSPSTDOUT &LOGSTDOUT +
                          &PRTSTDOUT &DLTSTDOUT)

             DCL        VAR(&VIEWOUTPUT) TYPE(*CHAR) LEN(5)
             DCL        VAR(&OUTPUTTYPE) TYPE(*CHAR) LEN(10)
             DCL        VAR(&DBHOST) TYPE(*CHAR) LEN(100)
             DCL        VAR(&DBNAME) TYPE(*CHAR) LEN(100)
             DCL        VAR(&DBUSER) TYPE(*CHAR) LEN(50)
             DCL        VAR(&DBPASS) TYPE(*CHAR) LEN(50)
             DCL        VAR(&DBPORT) TYPE(*CHAR) LEN(5)
             DCL        VAR(&PROMPT) TYPE(*CHAR) LEN(4)
             DCL        VAR(&SCRIPTFILE) TYPE(*CHAR) LEN(255)
             DCL        VAR(&FIELDDELIM) TYPE(*CHAR) LEN(2)
             DCL        VAR(&DBFILE) TYPE(*CHAR) LEN(255)
             DCL        VAR(&SQL) TYPE(*CHAR) LEN(4000)
             DCL        VAR(&CMDARGS) TYPE(*CHAR) LEN(4000)
             DCL        VAR(&ACTION) TYPE(*CHAR) LEN(50)
             DCL        VAR(&OUTPUTFILE) TYPE(*CHAR) LEN(255)
             DCL        VAR(&REPLACE) TYPE(*CHAR) LEN(5)
             DCL        VAR(&THROTTLEMS) TYPE(*CHAR) LEN(5)
             DCL        VAR(&OUTFILE) TYPE(*CHAR) LEN(20)
             DCL        VAR(&OFILE) TYPE(*CHAR) LEN(10)
             DCL        VAR(&OLIB) TYPE(*CHAR) LEN(10)
             DCL        VAR(&WORKDIR) TYPE(*CHAR) LEN(255)
             DCL        VAR(&EXEFILE) TYPE(*CHAR) LEN(255)
             DCL        VAR(&EXEFULL) TYPE(*CHAR) LEN(255)
             DCL        VAR(&DSPSTDOUT) TYPE(*CHAR) LEN(4)
             DCL        VAR(&LOGSTDOUT) TYPE(*CHAR) LEN(4)
             DCL        VAR(&PRTSTDOUT) TYPE(*CHAR) LEN(4)
             DCL        VAR(&DLTSTDOUT) TYPE(*CHAR) LEN(4)
             DCL        VAR(&DSPSTDOUT) TYPE(*CHAR) LEN(4)
             DCL        VAR(&DLTSTDOUT) TYPE(*CHAR) LEN(4)
             MONMSG     MSGID(CPF0000) EXEC(GOTO CMDLBL(ERRORS))

/*----------------------------------------------------------------------------*/
/* Parse outfile parm */
/*----------------------------------------------------------------------------*/
             CHGVAR     VAR(&OLIB) VALUE(%SST(&OUTFILE 11 10))
             CHGVAR     VAR(&OFILE) VALUE(%SST(&OUTFILE 1 10))

/*----------------------------------------------------------------------------*/
/* Make sure Python script exists */
/*----------------------------------------------------------------------------*/
             QSHONI/QSHIFSCHK FILNAM(&SCRIPTFILE)
             /* Script nout found. Bail out */
             MONMSG     MSGID(CPF9898) EXEC(DO)
             SNDPGMMSG  MSGID(CPF9898) MSGF(QCPFMSG) MSGDTA('Script +
                          file' |> &SCRIPTFILE |> 'not found. +
                          Native ibm_db CLI Process cancelled') +
                          MSGTYPE(*ESCAPE)
             ENDDO
             /* Script exists. Do nothing */
             MONMSG     MSGID(CPF9897) EXEC(DO)
             ENDDO

/*----------------------------------------------------------------------------*/
/* Run the Python script file */
/*----------------------------------------------------------------------------*/
             CHGVAR     VAR(&CMDARGS) VALUE('python3 ' |> &SCRIPTFILE)
             CHGVAR     VAR(&CMDARGS) VALUE(&CMDARGS |> '--action "' |< &ACTION |< '"')
             CHGVAR     VAR(&CMDARGS) VALUE(&CMDARGS |> '--outputfile "' |< &OUTPUTFILE  |< '"')
             CHGVAR     VAR(&CMDARGS) VALUE(&CMDARGS |> '--replace "' |< &REPLACE |< '"')
             CHGVAR     VAR(&CMDARGS) VALUE(&CMDARGS |> '--delimiter "' |< &FIELDDELIM |<  '"')
             CHGVAR     VAR(&CMDARGS) VALUE(&CMDARGS |> '--outputtype "' |< &OUTPUTTYPE |< '"')
             CHGVAR     VAR(&CMDARGS) VALUE(&CMDARGS |> '--sql "' |< &SQL |< '"')

             IF         COND(&PROMPT *EQ *YES) THEN(DO)
             ?          QSHONI/QSHEXEC ??CMDLINE(&CMDARGS) +
                          ??DSPSTDOUT(&DSPSTDOUT) +
                          ??LOGSTDOUT(&LOGSTDOUT) +
                          ??PRTSTDOUT(&PRTSTDOUT) +
                          ??DLTSTDOUT(&DLTSTDOUT)
             ENDDO
             IF         COND(&PROMPT *NE *YES) THEN(DO)
             QSHONI/QSHEXEC CMDLINE(&CMDARGS) DSPSTDOUT(&DSPSTDOUT) +
                          LOGSTDOUT(&LOGSTDOUT) +
                          PRTSTDOUT(&PRTSTDOUT) DLTSTDOUT(&DLTSTDOUT)
             ENDDO

             /* View output file after creation if selected */
             IF         COND(&VIEWOUTPUT *EQ *YES) THEN(DO)
             EDTF       STMF(&OUTPUTFILE)
             ENDDO

             IF         COND(&ACTION *EQ 'query') THEN(DO)
             SNDPGMMSG  MSGID(CPF9898) MSGF(QCPFMSG) +
                          MSGDTA('Native ibm_db database query ran +
                          successfully to file' |> &OUTPUTFILE) +
                          MSGTYPE(*COMP)
             ENDDO
             IF         COND(&ACTION *NE 'query') THEN(DO)
             SNDPGMMSG  MSGID(CPF9898) MSGF(QCPFMSG) +
                          MSGDTA('Native ibm_db database nonquery command ran +
                          successfully') +
                          MSGTYPE(*COMP)
             ENDDO

             RETURN

/*----------------------------------------------------------------------------*/
/* HANDLE ERRORS     */
/*----------------------------------------------------------------------------*/
ERRORS:

             SNDPGMMSG  MSGID(CPF9898) MSGF(QCPFMSG) MSGDTA('Error +
                          occurred while running Native ibm_db database command. +
                          Please check the joblog') MSGTYPE(*ESCAPE)

             ENDPGM
