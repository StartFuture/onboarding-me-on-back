from app.dao.dao import connect_database


def select_pack(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT tracking_code, status, employee_id, welcome_kit_id from Tracking
    WHERE employee_id = {employee_id}
    ;
    """

    try:
        cursor.execute(query)
    except:
        pack = None
    else:
        pack = cursor.fetchone()
    finally:
        connection.close()

    return pack


def insert_pack(employee_id: int, welcome_kit_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO Tracking(employee_id, welcome_kit_id, status) 
    VALUES 
    ('{employee_id}', '{welcome_kit_id}', 'to_be_send');
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    finally:
        connection.commit()
        connection.close()

    return True

def update_track_status_to_sended(tracking_id: int, tracking_code: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE onboarding_me.Tracking
    SET status='sended', tracking_code='{tracking_code}'
    WHERE id = {tracking_id}
    ;
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    finally:
        connection.commit()
        connection.close()
        
    return True


def update_track_status_to_delivered(tracking_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE onboarding_me.Tracking
    SET status='delivered'
    WHERE id = {tracking_id}
    ;

    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    finally:
        connection.commit()
        connection.close()

    return True



def verify_if_tracking_exists(tracking_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id, tracking_code, status, employee_id, welcome_kit_id
    FROM onboarding_me.Tracking
    WHERE id = {tracking_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        tracking_exists = cursor.fetchone()
        
        if tracking_exists:
            return True
        
    return False
    
