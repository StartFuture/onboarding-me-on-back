from app.dao.dao import connect_database


def select_company_password(user_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT company_password
    FROM Company
    WHERE id = {user_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        company_password = cursor.fetchone()
        connection.close()
        
        return company_password
    

def update_password(new_password: str, user_id: int):
    
    connection, cursor = connect_database()
    
    query =f"""
    UPDATE Company
    SET company_password = '{new_password}'
    WHERE id = {user_id}
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