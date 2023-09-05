from app.dao.dao import connect_database

def select_pack(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT tracking_code, status, tracking_id, employee_id, welcome_kit_id from Tracking
	WHERE employee_id = '{employee_id}';
    """

    try:
        cursor.execute(query)
    except:
        pack = None
    else:
        pack = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return pack

def insert_pack(employee_id: int, welcome_kit_id: int, tracking_code: str, status: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO Tracking(employee_id, welcome_kit_id, tracking_code, status) VALUES ('{employee_id}', '{welcome_kit_id}', '{tracking_code}', '{status}');
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    finally:
        connection.commit()
        connection.close()

    return True

def update_track(status: str, tracking_code: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE Tracking
	set status = '{status}'
	WHERE tracking_code = '{tracking_code}';
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return None
    finally:
        connection.commit()
        connection.close()

    return True