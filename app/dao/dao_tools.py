from datetime import datetime

from app.dao.dao import connect_database
from app.schemas.tool import Tool, EmployeeTool
from app.schemas.category_tool import CategoryTool


def select_tools(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT t.name, t.link_download, t.score, t.game_id, ct.name as category_name FROM Tool t
	right join CategoryTool ct on t.category_id = ct.id 
    left join Game g on g.id = t.game_id 
    left join GamifiedJourney gj on gj.id = g.gamified_journey_id 
    left join Company c on c.id = gj.company_id 
    WHERE
    c.id = {company_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
        
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
    ('{tool.link_download}', '{tool.name}', {tool.score}, {tool.game_id}, {tool.category_id})
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
    

def update_tool(tool: Tool):

    connection, cursor = connect_database()

    query = f"""
    UPDATE Tool
    SET link_download = '{tool.link_download}', name = '{tool.name}', score = {tool.score}, category_id = {tool.category_id} 
    WHERE id = {tool.id_tool};
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


def delete_tool(tool_id : int, game_id: int):

    connection, cursor = connect_database()
    
    list_tool = [{'id': tool_id}]
    
    deleted_link_tool = delete_linked_tool(list_tool)
    
    if not deleted_link_tool:
        return False
    

    query = f"""
    DELETE FROM Tool
    WHERE game_id = {game_id} and id = {tool_id}
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
    
    
def verify_tool_exists(name: str = None, id_tool: int = None):

    connection, cursor = connect_database()

    if id_tool:
        query = f"SELECT id FROM Tool WHERE id = {id_tool}"
    else:
        query = f"SELECT id FROM Tool WHERE name = {name}"
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        tool_id = cursor.fetchone()
        connection.close()
        
        return bool(tool_id)


def insert_category_tool(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO CategoryTool 
    (name)
    VALUES
    ('{category_tool.name}')
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        connection.commit()
        
        query = f'SELECT LAST_INSERT_ID() FROM CategoryTool;'
        cursor.execute(query)
        
        category_tool_id = cursor.fetchone()
        connection.close()

        return category_tool_id
    

def update_category_tool(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE CategoryTool
    SET name = '{category_tool.name}'
    WHERE id = {category_tool.category_tool_id}
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
    
    
def select_all_tools_by_category_id(category_tool_id: int, company_id: int):

    connection, cursor = connect_database()
    
    query = f"""
    SELECT t.id FROM onboarding_me.CategoryTool ct
    LEFT JOIN Tool t ON t.category_id = ct.id
    LEFT JOIN Game g ON g.id = t.game_id 
    LEFT JOIN GamifiedJourney gj ON gj.id = g.gamified_journey_id 
    LEFT JOIN Company c ON c.id = gj.company_id 
    WHERE ct.id = {category_tool_id} and c.id = {company_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        list_tools_id = cursor.fetchall()
        connection.close()
        
        return list_tools_id
         

def delete_all_tools_from_a_category(category_id: int, list_tools: list):
    
    connection, cursor = connect_database()
    
    ids = [tool['id'] for tool in list_tools]
 
    placeholder = ','.join(['%s'] * len(ids))
    
    query = f"""
    DELETE FROM Tool  
    WHERE category_id = %s AND id IN ({placeholder})
    ;
    """
    
    try:
        params = (category_id, ) + tuple(ids)
        cursor.execute(query, params)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        
        return True
    
    
def delete_linked_tool(list_tools: list) :
    
    connection, cursor = connect_database()
    
    ids = [tool['id'] for tool in list_tools]
 
    placeholder = ','.join(['%s'] * len(ids))
    
    query = f"""
    DELETE FROM onboarding_me.Employee_Tool
    WHERE tool_id IN ({placeholder})
    ;
    """
    
    try:
        cursor.execute(query, ids)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        
        return True
        

def delete_category_tool(category_tool_id: int, company_id: int):
    
    connection, cursor = connect_database()
    
    list_tools_id = select_all_tools_by_category_id(category_tool_id, company_id)
    
    if not list_tools_id: 
        return False
    
    linked_tools_deleted = delete_linked_tool(list_tools_id)
    
    if not linked_tools_deleted: 
        return False 
        
    tools_deleted = delete_all_tools_from_a_category(category_tool_id, list_tools_id)
    
    if not tools_deleted: 
        return False
            
    query = f"""
    DELETE FROM CategoryTool
    WHERE id = {category_tool_id}
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


def verify_if_category_exists(category_name: str = None, category_id: int = None):
    
    connection, cursor = connect_database()
    
    if category_name:
    
        query =f"""
        SELECT name From CategoryTool ct WHERE name = '{category_name}'
        ;
        """
        
    if category_id:
        
        query =f"""
        SELECT id From CategoryTool ct WHERE id = '{category_id}'
        ;
        """
    
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False    
    
    else:    
        
        category_exists = cursor.fetchone()
        connection.close()
        
        if category_exists:
            return True
        
    return False


def linking_tool(employee_tool: EmployeeTool):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO Employee_Tool (employee_id, tool_id, nick_name)
    VALUES ({employee_tool.employee_id}, {employee_tool.tool_id}, '{employee_tool.nick_name}');
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


def verify_tool_completed(tool_id: int = None, employee_tool_id: int = None):

    connection, cursor = connect_database()

    if employee_tool_id:
        query = f"SELECT id FROM Employee_Tool WHERE id = {employee_tool_id}"
    else:
        query = f"SELECT id FROM Employee_Tool WHERE tool_id = {tool_id}"
    
    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        tool_id = cursor.fetchone()

        connection.close()

        return bool(tool_id)


def get_tool_score(employee_tool: EmployeeTool):

    connection, cursor = connect_database()

    query = f"""
    SELECT t.score FROM Employee_Tool et LEFT JOIN
    Tool t ON t.id = {employee_tool.tool_id};
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return 0
    else:
        score = cursor.fetchone()

        connection.close()

        return score["score"]
    
    
def get_game_id_tool(employee_tool: EmployeeTool):

    connection, cursor = connect_database()

    query = f"""SELECT t.game_id FROM Employee_Tool et LEFT JOIN
    Tool t ON t.id = {employee_tool.tool_id};
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return None
    else:
        game_id = cursor.fetchone()

        connection.close()

        return game_id["game_id"]
    
    
def sum_score(game_id: int):

    connection, cursor = connect_database()

    query = f'SELECT total_points FROM Score WHERE game_id = {game_id}'

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close
        return None
    
    else:
        
        points = cursor.fetchone()
        connection.close()

        return points["total_points"]
    

def saving_tool_score(employee_tool: EmployeeTool, score_exists: bool = False):

    last_updated = datetime.now()

    connection, cursor = connect_database()

    score = get_tool_score(employee_tool)

    game_id = get_game_id_tool(employee_tool)


    if score_exists:
        score += sum_score(game_id)
        query = f"""
        UPDATE Score set total_points = {score}, last_updated = '{last_updated}'
        WHERE game_id = {game_id};
        """
    else:
        query = f"""
        INSERT INTO Score (total_points, last_updated, employee_id, game_id)
        VALUES ({score}, '{last_updated}', {employee_tool.employee_id}, {game_id});
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
    
    

def verify_score_tool_exists(game_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT id FROM Score WHERE game_id = {game_id}
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        game_id = cursor.fetchone()

        connection.close()

        return 1 if bool(game_id) else 0


def get_count_tools(gamified_journey: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT COUNT(t.id) FROM GamifiedJourney gj  
    LEFT JOIN Game g ON g.gamified_journey_id  = gj.id
    LEFT JOIN Tool t ON t.game_id = g.id
    WHERE gj.id = {gamified_journey};
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return None
    else:
        tools_id = cursor.fetchone()

        connection.close()
        
        return tools_id["COUNT(t.id)"]


def ended_game_tools(employee_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT COUNT(et.id) FROM Employee e LEFT JOIN 
    Employee_Tool et ON et.employee_id = {employee_id};
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return None
    else:
        tools_completed = cursor.fetchone()

        connection.close()

        return tools_completed["COUNT(et.id)"]
