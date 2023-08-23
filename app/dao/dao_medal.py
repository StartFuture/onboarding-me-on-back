from app.dao.dao import connect_database

def select_medal(medal_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT name, image, medal_id from GamifiedJourney
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

def insert_medal(medal_id: int, score_id):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO Medal_Score(medal_id, score_id) VALUES ('{medal_id}','{score_id}');
    """
    
    try:
        cursor.execute(query)
    except:
        None
    finally:
        connection.commit()
        connection.close()

    return True
