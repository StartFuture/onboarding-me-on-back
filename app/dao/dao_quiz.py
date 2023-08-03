from app.dao.dao import connect_database

def select_quiz(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT q.title, q.score  FROM Quiz q
    left join Game g on g.id = q.game_id 
    left join GamifiedJourney gj on gj.id = g.gamified_journey_id 
    left join Company c on c.id = gj.company_id 
    WHERE
    c.id ={id}
    ;
    """

    cursor.execute(query)
    
    quiz_list = cursor.fetchall()
    
    connection.close()

    return quiz_list