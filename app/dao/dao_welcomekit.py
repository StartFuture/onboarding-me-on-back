from app.dao.dao import connect_database

from app.schemas.tracking_code import TrackingCode

def select_tracking(employee_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT tracking_code, status 
    FROM onboarding_me.Tracking
    WHERE employee_id = {employee_id}
    ;
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return None
    
    else: 
        status = cursor.fetchone()
        connection.close()
        return status
    
def insert_tracking(employee_id, welcome_kit_id: int):
    
    connection,cursor = connect_database()

    query = f"""
    INSERT INTO onboarding_me.Tracking
    (status, employee_id, welcome_kit_id)
    VALUES('to_be_send', {employee_id}, {welcome_kit_id})
    ;
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        return True
    
def update_tracking_status_sended(tracking_code: TrackingCode):
    
    connection,cursor = connect_database()

    query = f"""
    UPDATE onboarding_me.Tracking
    SET tracking_code='{tracking_code.tracking_code}', status='sended'
    WHERE employee_id={tracking_code.employee_id}
    ;
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        return True
    
def update_tracking_status_delivered(employee_id: int):
    connection,cursor = connect_database()

    query = f"""
    UPDATE onboarding_me.Tracking
    SET status='delivered'
    WHERE employee_id = {employee_id}
    ;
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        return True