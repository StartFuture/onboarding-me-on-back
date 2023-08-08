from app.dao.dao import connect_database
from app.schemas.tool import Tool

def select_tool(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT t.name, t.score FROM Tool t
    left join Game g on g.id = t.game_id 
    left join GamifiedJourney gj on gj.id = g.gamified_journey_id 
    left join Company c on c.id = gj.company_id 
    WHERE
    c.id ={id}
    ;
    """

    cursor.execute(query)
    
    tool_list = cursor.fetchall()
    
    connection.close()

    return tool_list

def insert_tool(tool: Tool):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO Tool 
    (link_download, name, score, game_id, category_id)
    VALUES
    ('{tool.link_download}', '{tool.name}', {tool.score}, 1, 1);
    """

    cursor.execute(query)
    connection.commit()

    query = f'SELECT name FROM Tool WHERE name = "{tool.name}"'

    cursor.execute(query)
    tool_result = cursor.fetchone()
    connection.close()

    return tool_result

def update_tool(tool: Tool):

    connection, cursor = connect_database()

    query = f"""
    UPDATE Tool
    SET link_download = '{tool.link_download}', name = '{tool.name}', score = {tool.score} 
    WHERE id = 3;
    """

    cursor.execute(query)
    connection.commit()

    query = f'SELECT name FROM Tool WHERE name = "{tool.name}";'

    cursor.execute(query)
    tool_result = cursor.fetchone()
    connection.close()

    return tool_result


#def verify_tool_exists(tool: Tool):