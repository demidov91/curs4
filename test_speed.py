import psycopg2
from py2neo import neo4j

import datetime


def pgsql_get_connection():
    return psycopg2.connect(database="test_speed", user="curs", port="5432", host="localhost", password="curs")
    
def pgsql_drop_data():
    conn  = pgsql_get_connection()
    curs = conn.cursor()
    curs.execute("DELETE FROM knows;");
    curs.execute("DELETE FROM curs_user;")
    conn.commit()
    curs.close
    conn.close()


def get_batch_data():
    return list({'email': '{0}@{0}.{1}'.format(i, i+1), 'name': '{0}{0}{0}'.format(i)} for i in xrange(500))


def get_pgsql_request(data):
    rendered_data = ', '.join("('{email}', '{name}')".format(**entry) for entry in data)
    return 'INSERT INTO curs_user (email, name) VALUES '+ rendered_data + ';'

def get_pgsql_formatted_request(data):
    data_format = ', '.join("(%s, %s)" for x in xrange(len(data)))
    return 'INSERT INTO curs_user (email, name) VALUES '+ data_format + ';'

def pgsql_prepare_connections(conn):
    curs = conn.cursor()
    curs.execute("SELECT id FROM curs_user;");
    ids = list(x[0] for x in curs.fetchall())
    l = len(ids)
    for index, id in enumerate(ids):
        curs.execute("INSERT INTO knows (owner_id, recipient_id) VALUES(%s, %s), (%s, %s), (%s, %s), (%s, %s);",\
         (ids[index], ids[(index+1) % l], ids[index], ids[(index+2) % l], ids[index], ids[(index+3) % l], ids[index], ids[(index+4) % l] ))
    conn.commit()
    curs.close()
    return ids
    
def pgsql_get_connections(ids):
    for id in ids:
        conn = psycopg2.connect(database="test_speed", user="curs", port="5432", host="localhost", password="curs")
        curs = conn.cursor()
        curs.execute("SELECT email FROM knows, curs_user WHERE knows.owner_id=%s and knows.recipient_id=curs_user.id;", (id, ))
        curs.fetchall()
        curs.close()
        conn.close()
        
def pgsql_stored_get_connections(ids):
    for id in ids:
        conn = psycopg2.connect(database="test_speed", user="curs", port="5432", host="localhost", password="curs")
        curs = conn.cursor()
        curs.execute("SELECT * FROM select_connected_users(%s);", (id, ))
        curs.fetchall()
        curs.close()
        conn.close()


def gen_values(data):
    for item in data:
        yield item['email']
        yield item['name']


def pgsql_batch_insert():
    conn = psycopg2.connect(database="test_speed", user="curs", port="5432", host="localhost", password="curs")
    data = get_batch_data()
    statement = get_pgsql_formatted_request(data)
    start = datetime.datetime.now()
    curs = conn.cursor()
    curs.execute(statement, list(gen_values(data)))
    conn.commit()
    curs.close()
    stop = datetime.datetime.now()
    print stop - start
    conn.close()
    
    
def prepare_neo4j():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7475/db/data/")    
    graph_db.clear()
    graph_db.get_or_create_index(neo4j.Node, "users")
    return graph_db
    
def neo4j_batch_insert():
    data = get_batch_data()
    graph_db = prepare_neo4j()
    start = datetime.datetime.now()
    
    index = graph_db.get_or_create_index(neo4j.Node, "users")
    batch = neo4j.WriteBatch(graph_db)
    for entry in data:
        batch.create_indexed_node_or_fail(index, 'email', entry['email'], entry)
    items = batch.submit()
    stop = datetime.datetime.now()
    print stop - start
    return items
    
def psql_o_b_o():
    data = get_batch_data()
    conn = psycopg2.connect(database="test_speed", user="curs", port="5432", host="localhost", password="curs")
    start = datetime.datetime.now()
    for index, item in enumerate(data):
        curs = conn.cursor()
        curs.execute("INSERT INTO curs_user (email, name) VALUES (%s, %s)", (item['email'], item['name']))
        conn.commit()
        curs.close()       
    stop = datetime.datetime.now()
    print stop - start
    conn.close()
    
def neo4j_o_b_o():
    data = get_batch_data()
    graph_db = prepare_neo4j()
    start = datetime.datetime.now()
    
    index = graph_db.get_or_create_index(neo4j.Node, "users")
    for entry in data:
        index.create_if_none('email', entry['email'], entry)
    stop = datetime.datetime.now()
    print stop - start
    
def pgsql_connections():
    pgsql_batch_insert()
    conn = pgsql_get_connection()
    ids = pgsql_prepare_connections(conn)
    conn.close()
    start = datetime.datetime.now()
    
    pgsql_get_connections(ids)
    
    stop = datetime.datetime.now()
    print stop - start
    pgsql_drop_data()
    
    
def neo4j_prepare_connections(db):    
    items = neo4j_batch_insert()
    batch = neo4j.WriteBatch(db)
    for i in xrange(len(items)):
        batch.create_relationship(items[i], 'KNOWS', items[(i+1) % len(items)])
        batch.create_relationship(items[i], 'KNOWS', items[(i+2) % len(items)])
        batch.create_relationship(items[i], 'KNOWS', items[(i+3) % len(items)])
        batch.create_relationship(items[i], 'KNOWS', items[(i+4) % len(items)])
    batch.submit()
    return items
    
    
def neo4j_get_connections(items):
    for item in items:
        item.get_related_nodes(0, 'KNOWS')
    
    
def neo4j_connections():
    db = prepare_neo4j()
    items = neo4j_prepare_connections(db)
    start = datetime.datetime.now()
    
    neo4j_get_connections(items)
    
    stop = datetime.datetime.now()
    print stop - start


    
    
    
def pgsql_stored():
    pgsql_batch_insert()
    conn = pgsql_get_connection()
    ids = pgsql_prepare_connections(conn)
    conn.close()
    start = datetime.datetime.now()
    
    pgsql_stored_get_connections(ids)
    
    stop = datetime.datetime.now()
    print stop - start
    
    pgsql_drop_data()
    

def run():
    pgsql_batch_insert()
    pgsql_drop_data()
    
if __name__ == '__main__':
    run()