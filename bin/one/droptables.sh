#!/bin/bash
export PGUSER=one
export PGDB=one
export PGPASSWORD=(kx^@61sl(3*p5di7hue=wh10aj1$#1=v_r&vj^r=vdqc9(5&@

pg_dump -U ${PGUSER} ${PGDB} -f database_dump.sql

psql -U ${PGUSER} ${PGDB} -t -c "select 'drop table \"' || tablename || '\" cascade;' from pg_tables where schemaname = 'public'" | psql -U ${PGUSER} ${PGDB}

#pg_dump -U ${PGUSER} -d ${PGDB} -f database_dump.sql