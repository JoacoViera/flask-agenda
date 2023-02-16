from flaskext.mysql import MySQL

def select(connection, selectStm, data):
    try:
        connection.connect()
        cursor = connection.cursor()
        cursor.execute(selectStm, data)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    except Exception as e:
        print("Problem selecting into db: " + str(e))
        return []
    return []
    
def insert(connection, insertStm, data):
    try:
        connection.connect()
        cursor = connection.cursor()
        cursor.execute(insertStm, data)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return False
    return False

def insert_id(connection, insertStm, data):
    try:
        connection.connect()
        cursor = connection.cursor()
        cursor.execute(insertStm, data)
        connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return new_id
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return []
    return []

def delete(connection, insertStm, data):
    try:
        connection.connect()
        cursor = connection.cursor()
        cursor.execute(insertStm, data)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Problem deleting into db: " + str(e))
        return False
    return False

def update(connection, insertStm, data):
    try:
        connection.connect()
        cursor = connection.cursor()
        cursor.execute(insertStm, data)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Problem updating into db: " + str(e))
        return False
    return False

