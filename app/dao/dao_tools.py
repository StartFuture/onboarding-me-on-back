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

    try:
        cursor.execute(query)
    except Exception as error:
        return False
    else:
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
    try:
        cursor.execute(query)
    except Exception as error:
        return None
    else:
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
    WHERE id = {tool.id_tool};
    """
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    else:
        connection.commit()
        connection.close()

        return True


def verify_tool_exists(name: str = None, id_tool: int = None):

    connection, cursor = connect_database()

    if id_tool:
        query = f"SELECT id FROM Tool WHERE id = {id_tool}"
    else:
        query = f"SELECT id FROM Tool WHERE id = {name}"
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    else:
        tool_id = cursor.fetchone()

        connection.close()

        return bool(tool_id)
    
