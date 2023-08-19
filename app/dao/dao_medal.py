from app.dao.dao import connect_database

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
