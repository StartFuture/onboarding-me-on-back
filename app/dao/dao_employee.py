from datetime import datetime
from decimal import Decimal

from app.dao.dao import connect_database
from app.schemas.quiz import EmployeeAlternative
from app.dao.dao_tools import sum_score
from app.dao.dao_quiz import get_max_score

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
            score += sum_score(game_id)
            query = f"""
            UPDATE Score set total_points = {score}, last_updated = '{last_updated}'
            WHERE game_id = {game_id} and employee_id = {employee_alternative.employee_id}
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
         
         score_value = score['total_points']
         
         return score_value   
     
     
def insert_medal_score(employee_id: int, game_id:int, score_id: int):
    
    
    connection, cursor = connect_database()  
    
    max_score = get_max_score(game_id=game_id)
        
    employee_total_score = get_total_score(employee_id=employee_id,game_id=game_id)
    
    bronze_medal =  max_score * Decimal(0.50)
    
    silver_medal =  max_score * Decimal(0.90)
    
    
    if employee_total_score <= bronze_medal:
        
        query = f"""
        INSERT INTO onboarding_me.Medal_Score
        (medal_id, score_id)
        VALUES(3, {score_id});
        """
        
    elif employee_total_score <= silver_medal:
        
        query = f"""
        INSERT INTO onboarding_me.Medal_Score
        (medal_id, score_id)
        VALUES(2, {score_id});
        """
        
    else:
        
        query = f"""
        INSERT INTO onboarding_me.Medal_Score
        (medal_id, score_id)
        VALUES(1, {score_id});
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
    

def get_medal_score(employee_id: int, game_id: int):

    connection, cursor = connect_database()
    
    query = f"""
    SELECT medal_id FROM Medal_Score ms
    RIGHT JOIN Score s ON s.id = ms.score_id 
    RIGHT JOIN Employee e ON e.id = s.employee_id 
    WHERE e.id = {employee_id} and s.game_id = {game_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
        
    else:

        medals_list = cursor.fetchall()
        connection.close()
        
        return medals_list



def get_employee_medals(employee_id: int, game_id: int):
    
    
    connection, cursor = connect_database()

    medals_list = get_medal_score(employee_id=employee_id, game_id=game_id)

    medals_id = []
        
    for medals in medals_list:
        medals_id.append(medals['medal_id']) 
    
    
    placeholder = ','.join(['%s'] * len(medals_list))
    
    query = f"""
    SELECT m.name, m.image FROM Medal m 
    RIGHT JOIN Medal_Score ms on ms.medal_id = m.id 
    RIGHT JOIN Score s ON s.id = ms.score_id 
    RIGHT JOIN Employee e ON e.id = s.employee_id 
    WHERE m.id IN ({placeholder}) and e.id = %s
    ;
    """
    
    try:
        cursor.execute(query, medals_id + [employee_id])

    except Exception as error:
        connection.close()
        return []

    else:
            
        employee_medals_list = cursor.fetchall()
        connection.close()
             
        return employee_medals_list

          
def verify_employee_exists(employee_id: int, company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id
    FROM onboarding_me.Employee
    WHERE id = {employee_id} and company_id = {company_id};
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
  

def verify_alternative_exists(alternative_id: int, quiz_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id
    FROM onboarding_me.Alternative
    WHERE id = {alternative_id} and quiz_id = {quiz_id} 
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


def verify_quiz_completed(quiz_id: int, employee_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT a.id
    FROM onboarding_me.Employee_Alternative ea
    LEFT JOIN Alternative a on a.id = ea.alternative_id 
    WHERE a.quiz_id = {quiz_id} and ea.employee_id = {employee_id}
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
    
    
def verify_score_quiz_exists(game_id: int, employee_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT id FROM Score WHERE game_id = {game_id} and employee_id = {employee_id}
    ;
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
    

def get_count_employee_answers(employee_id: int):
    
    
    connection, cursor = connect_database()

    query = f"""
    SELECT COUNT(id) FROM Employee_Alternative ea 
    WHERE employee_id = {employee_id}
    ;
    """

    cursor.execute(query)

    count_answers = cursor.fetchone()
    connection.close()

    return count_answers
    

def get_count_quiz(game_id: int):
    
    
    connection, cursor = connect_database()

    query = f"""
    SELECT COUNT(id) FROM Quiz q 
    WHERE game_id  = {game_id}
    ; 
    """

    cursor.execute(query)

    count_quiz = cursor.fetchone()
    connection.close()

    return count_quiz
    
    
def finished_quiz_game(employee_id: int, game_id: int):
    

    try:
        count_quiz = get_count_quiz(game_id=game_id)
        count_answers = get_count_employee_answers(employee_id=employee_id)
        
    except Exception as error:
        return False
    
    else:

        if count_answers != count_quiz:
            return False
           
    return True
 
