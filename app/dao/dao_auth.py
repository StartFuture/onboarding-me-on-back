from app.dao.dao import connect_database


def select_revoked_token(user_id: int, token: str):
    
    connection, cursor = connect_database()
        
    query = f"""
    SELECT user_id, token
    FROM onboarding_me.Revoked_Tokens
    WHERE token  = '{token}' and user_id = {user_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        revoked_token = cursor.fetchone()
        connection.close()
        
        return revoked_token


def insert_revoked_tokens(user_id: int, token: str):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO onboarding_me.Revoked_Tokens
    (user_id, token)
    VALUES
    ({user_id}, '{token}')
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


