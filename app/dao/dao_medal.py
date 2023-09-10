from app.dao.dao import connect_database


def select_medal(medal_id, game_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT name, image, game_id
    FROM onboarding_me.Medal
    WHERE id = {medal_id} and game_id = {game_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        medal_data = cursor.fetchone()
        connection.close()
        
        medal_data["image"] = medal_data["image"].decode('utf-8')

        return medal_data
    
    
def insert_medal(name, image: str, game_id: int):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO onboarding_me.Medal
    (name, image, game_id)
    VALUES
    ('{name}', '{image}', '{game_id}')
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
    
    
def update_medal(medal_id: int, name, image: str):

    connection, cursor = connect_database()

    query = f"""
    UPDATE onboarding_me.Medal
    SET name = '{name}', image = '{image}'
    WHERE id = {medal_id}
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
    
    
def delete_linked_medal(medal_id: int):

    connection, cursor = connect_database()

    query = f"""
    DELETE FROM onboarding_me.Medal_Score
    WHERE medal_id = {medal_id}
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
    
    
def delete_medal(medal_id: int):

    connection, cursor = connect_database()
    
    medal_linked_deleted = delete_linked_medal(medal_id)
    
    if not medal_linked_deleted:
        return False
    
    query = f"""
    DELETE FROM onboarding_me.Medal
    WHERE id = {medal_id}
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
 
 
def verify_if_medal_exists(medal_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT name
    FROM onboarding_me.Medal
    WHERE id = {medal_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        medal_exists = cursor.fetchone()
        connection.close()
        
        if medal_exists:
            return True

        return False


