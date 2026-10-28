#!../../bin/linux-x86_64/softIocPy3.6

#- SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#-
#- SPDX-License-Identifier: EPICS

#- You may have to change alarmDemo to something else
#- everywhere it appears in this file

< envPaths

epicsEnvSet("PINI", "${PINI='NO'}")
epicsEnvSet("RVAL", "${RVAL='VAL'}")
epicsEnvSet("HASH", "${HASH='#'}")

py "import alarm"
py "alarm.build()"

## Load record instances
dbLoadRecords("db/alarm.db","PINI=${PINI}, RVAL=${RVAL}, HASH=${HASH}")

iocInit
dbDumpRecord > dbDumpRecord.log
