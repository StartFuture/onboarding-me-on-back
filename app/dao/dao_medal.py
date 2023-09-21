from app.dao.dao import connect_database


def select_medals(company_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT m.id, m.name, m.image  FROM onboarding_me.Medal m
    LEFT JOIN Game g ON m.game_id = g.id 
    LEFT JOIN GamifiedJourney gj ON g.gamified_journey_id = gj.id 
    LEFT JOIN Company c ON c.id = gj.company_id 
    WHERE c.id = {company_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        medals_data = cursor.fetchall()
        connection.close()
        
        if medals_data:
            for medal in medals_data:
                medal["image"] = medal["image"].decode('utf-8')

        return medals_data
    
    
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
