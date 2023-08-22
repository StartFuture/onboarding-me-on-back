from datetime import datetime

from app.dao.dao import connect_database
from app.schemas.quiz import EmployeeAlternative


def insert_employee_answer(employee_alternative: EmployeeAlternative):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO onboarding_me.Employee_Alternative
    (employee_id, alternative_id)
    VALUES
    ({employee_alternative.employee_id}, {employee_alternative.alternative_id})
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


def get_employee_answer(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT a.is_answer, q.score as quiz_score FROM Employee_Alternative ea 
    LEFT JOIN Alternative a ON a.id = ea.alternative_id 
    LEFT JOIN Quiz q ON q.id  = a.quiz_id 
    WHERE ea.employee_id = {employee_id}
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return None

    else:

         data_list = cursor.fetchall()
         connection.close()

         return data_list 
     
     
def get_game_id_quiz(alternative_id = int):
    
    connection, cursor = connect_database()

    query = f"""
    SELECT q.game_id FROM Alternative a 
    LEFT JOIN Quiz q on q.id = a.quiz_id 
    WHERE a.id = {alternative_id}
    ;
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
     
 
#USAR FUNÇÂO JÀ CRIADA PELO VICTOR APÓS ACEITAR O PR        
def sum_score_quiz(game_id: int):

    connection, cursor = connect_database()

    query = f'SELECT total_points FROM Score WHERE game_id = {game_id};'

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close
        return None
    
    else:
        points = cursor.fetchone()
        connection.close()

        return points["total_points"]     
        
    
def saving_employee_score(employee_alternative: EmployeeAlternative, score_exists: bool = False):
    
    connection, cursor = connect_database()
    
    last_updated = datetime.now()
    
    game_id = get_game_id_quiz(alternative_id= employee_alternative.alternative_id)
    
    data_list = get_employee_answer(employee_id= employee_alternative.employee_id)
    
    for data_dict in data_list:
        is_answer = data_dict['is_answer']
        score = data_dict['quiz_score']
         
    
    if is_answer == 1:
        
        if score_exists:
            score += sum_score_quiz(game_id)
            query = f"""
            UPDATE Score set total_points = {score}, last_updated = '{last_updated}'
            WHERE game_id = {game_id}
            ;
            """
        else: 
            query = f"""
            INSERT INTO Score 
            (total_points, last_updated, employee_id, game_id)
            VALUES 
            ({score}, '{last_updated}', {employee_alternative.employee_id}, {game_id})
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
          
    return False

        
def get_total_score(employee_id: int, game_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT total_points 
    FROM Score
    WHERE employee_id = {employee_id} AND game_id = {game_id}
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return None

    else:

         score = cursor.fetchone()
         connection.close()
         
         return score    
        
        
def verify_employee_exists(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id
    FROM onboarding_me.Employee
    WHERE id = {employee_id}
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return None

    else:

         employee_exists = cursor.fetchone()
         
         if employee_exists:
             return True
    
    return False


def verify_alternative_exists(alternative_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id
    FROM onboarding_me.Alternative
    WHERE id = {alternative_id}
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return False

    else:

         alternative_exists = cursor.fetchone()
         
         if alternative_exists:
             return True
    
    return False


def verify_quiz_completed(quiz_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT a.id
    FROM onboarding_me.Employee_Alternative ea
    LEFT JOIN Alternative a on a.id = ea.alternative_id 
    WHERE a.quiz_id = {quiz_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        quiz_completed = cursor.fetchone()
        connection.close()

        if quiz_completed:
            return True
        
    return False
    
    
def verify_score_quiz_exists(game_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT id FROM Score WHERE game_id = {game_id};
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        print(error)
        connection.close()
        return False
    
    else:
        game_id = cursor.fetchone()
        connection.close()

        return 1 if bool(game_id) else 0