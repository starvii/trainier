import sqlite3

import sys
import sqlite3
sys.path.append('../')
from trainier.util.object_id import object_id

conn = sqlite3.connect('C:/src/trainier/database/dev-db.sqlite')
# sql = 'select entityId from trunk order by rowid;'
# cx = conn.cursor()
# cx.execute(sql)
# r = cx.fetchall()
# # print(r)
# for eid, in r:
#     # print(eid)
#     trunk_id = object_id()
#     try:
#         cx.execute('BEGIN;')
#         cx.execute('update option set trunkId = ? where trunkId = ?;', (trunk_id, eid))
#         cx.execute('update trunk set entityId = ? where entityId = ?;', (trunk_id, eid))
#         cx.execute('COMMIT;')
#     except Exception:
#         cx.execute("ROLLBACK;")

sql = 'select entityId from option order by rowid;'
cx = conn.cursor()
cx.execute(sql)
r = cx.fetchall()
for eid, in r:
    opt_id = object_id()
    try:
        cx.execute('BEGIN;')
        cx.execute('update option set entityId = ? where entityId = ?', (opt_id, eid))
        cx.execute('COMMIT;')
    except Exception as e:
        cx.execute('ROLLBACK;')
        print(e)

conn.close()
