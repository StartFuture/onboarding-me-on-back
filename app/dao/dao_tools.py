from app.dao.dao import connect_database

def select_tool(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""SELECT t.name, t.score FROM Tool t
                    left join Game g on g.id = t.game_id 
                    left join GamifiedJourney gj on gj.id = g.gamified_journey_id 
                    left join Company c on c.id = gj.company_id 
                    WHERE
                    c.id = {id}
                    ;"""

    cursor.execute(query)
    
    tool_list = cursor.fetchall()
    
    connection.close()

    return tool_list