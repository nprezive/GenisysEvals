#!/bin/bash
NOW=$(date +"%Y%m%dT%H%M%SZ")
DUMP_FILENAME="$NOW"_genisys_db.sql
docker exec -it genisys_db_1 sh -c 'PGPASSWORD=$POSTGRES_PASSWORD pg_dumpall -U $POSTGRES_USER -h localhost -p 5432 --clean --file='$DUMP_FILENAME''
docker cp genisys_db_1:$DUMP_FILENAME .
docker exec -it genisys_db_1 rm $DUMP_FILENAME
echo $DUMP_FILENAME