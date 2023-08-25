from app.dao.dao import connect_database

def select_medal(medal_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT name, image, medal_id from Medal_Score
	WHERE medal_id = '{medal_id}';
    """

    try:
        cursor.execute(query)
    except:
        medal = None
    else:
        medal = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return medal

def insert_medal(medal_id: int, score_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO Medal_Score(medal_id, score_id) VALUES ('{medal_id}','{score_id}');
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    finally:
        connection.commit()
        connection.close()

    return True


def select_medal_by_employee(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT ms.medal_id from Score s 
    left join Medal_Score ms on s.id = ms.score_id 
    WHERE s.employee_id = {employee_id}
    ;
    """

    try:
        cursor.execute(query)
    except:
        medal = None
    else:
        medal = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return medal

def select_score_by_employee(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id from Score  
    WHERE employee_id = {employee_id}
    ;
    """

    try:
        cursor.execute(query)
    except:
        score_id = None
    else:
        score_id = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return score_id

def select_medal_by_game(game_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id from Medal m 
    WHERE game_id = {game_id}
    ;
    """

    try:
        cursor.execute(query)
    except:
        medal_id = None
    else:
        medal_id = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return medal_id