__author__ = 'ubriela'

import math
import psycopg2

def distance(lat1, lon1, lat2, lon2):
    """
    Distance between two geographical location
    """
    R = 6371  # km
    dLat = math.radians(abs(lat2 - lat1))
    dLon = math.radians(abs(lon2 - lon1))
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

conn = psycopg2.connect("dbname='iraindb' user='irain' host='localhost' password='chrs2014'")

cur = conn.cursor()

#cur.execute("SELECT t.taskid, t.place, ST_X(t.location), ST_Y(t.location), t.iscompleted FROM users u, tasks t  WHERE username = 'ubriela' AND u.userid=t.requesterid;")

cur.execute("SELECT t.taskid, r.worker_place, ST_X(r.worker_location), ST_Y(r.worker_location), t.place, ST_X(t.location), ST_Y(t.location), t.iscompleted, t.radius, t.type FROM users u, responses r, tasks t  WHERE u.userid=r.workerid AND r.taskid=t.taskid;")

rows = cur.fetchall()

print "\nShow me the databases:\n"
for row in rows:
    #print '\t'.join(map(str, row))
    # print row[0], "\t", row[2], "\t",row[3], "\t",row[5], "\t",row[6], "\t", distance(row[2],row[3],row[5],row[6]), "\t", row[len(row)-2], "\t", row[len(row)-1]
    if row[2] == 0 or row[4] == 0 or row[5] == 0 or row[6] == 0:
        continue
    # print row[2], "\t",row[3]
    print row[5], "\t",row[6]
conn.commit()

cur.close()

conn.close()