from typing import List

from app.dao.dao import connect_database
from app.schemas.quiz import Quiz, Alternative


def select_quiz(company_id: int = None):

    connection, cursor = connect_database()

    if company_id:
        
        query = f"""
        SELECT q.id, q.title, q.score  FROM Quiz q
        left join Game g on g.id = q.game_id 
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
        return False

    else:

         quiz_list = cursor.fetchall()
         connection.close()

         return quiz_list




def insert_quiz(quiz: Quiz):

    connection, cursor = connect_database() 
    
    query = f"""
    INSERT INTO Quiz 
    (link_video, score, title, question, quiz_type, game_id)
    VALUES
    ('{quiz.link_video}', {quiz.score}, '{quiz.title}', '{quiz.question}', '{quiz.quiz_type}', {quiz.game_id});
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return False
    
    else:

        query = "SELECT LAST_INSERT_ID() as id_quiz FROM Quiz;"

        cursor.execute(query)
        id_quiz = cursor.fetchone()
        connection.commit()

        connection.close()

        return id_quiz



def insert_alternatives(alternatives: list[Alternative], quiz_id: int):
    
    connection, cursor = connect_database()

    for alternative in alternatives:    
        
        query = f"""
        INSERT INTO Alternative 
        (alternative_text, is_answer, quiz_id)
        VALUES
        ('{alternative.text}', '{alternative.is_answer}', '{quiz_id}');
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


def update_quiz(quiz: Quiz):
   
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE Quiz 
    SET 
    link_video = '{quiz.link_video}', score = {quiz.score}, title = '{quiz.title}', question = '{quiz.question}', quiz_type = '{quiz.quiz_type}'
    WHERE id = '{quiz.quiz_id}' AND game_id = '{quiz.game_id}';
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


def delete_quiz_alternative(alternatives: List[int], quiz_id: int, game_id: int):
    
    connection, cursor = connect_database()
    
    try:
        
        connection.autocommit = False
        
        deleted = delete_alternative(connection=connection, cursor=cursor, alternatives=alternatives, quiz_id=quiz_id)
        
        if deleted:
            
            query = f"""
            DELETE FROM Quiz WHERE game_id = {game_id} and id = {quiz_id} 
            ;
            """     
            cursor.execute(query)
            
        
    except Exception as error:
        connection.close()
        return False
        
    else:
        connection.commit()
        connection.autocommit = True
        connection.close()
    
    return True


def delete_alternative(alternatives: List[int], quiz_id: int, connection = None, cursor = None):
   
    placeholder = ','.join(['%s'] * len(alternatives))
        
   
    if cursor and connection: 
        
        query = f"""
        DELETE FROM Alternative 
        WHERE quiz_id = %s AND id IN ({placeholder})
        ;
        """ 
          
        try:    
            cursor.execute(query, [quiz_id] + alternatives)
        
        except Exception as error:   
            connection.close()
            return False

        else:
            return True
    
    else:
        
        connection, cursor = connect_database()
        
        query = f"""
        DELETE FROM Alternative
        WHERE quiz_id = %s AND id IN ({placeholder})
        ;
        """
        
        try:
            cursor.execute(query, [quiz_id] + alternatives)
            
        except Exception as error:
            connection.close()
            return False

        else:
            
            connection.commit()
            connection.close()
        
            return True   
           

def update_alternative(alternatives: list[Alternative], quiz_id: int):

    
    for alternative in alternatives:
        
        connection, cursor = connect_database()

    
        query = f"""
        UPDATE Alternative  
        SET alternative_text  = '{alternative.text}', is_answer  = {alternative.is_answer}
        WHERE id = {alternative.alternative_id} AND quiz_id = {quiz_id};
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


def get_max_score(game_id: int):
    
    connection, cursor = connect_database()
        
    query = f"""
    SELECT SUM(score) FROM Quiz q 
    WHERE game_id = {game_id}
    ;
    """ 

    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return False

    else:

         max_score = cursor.fetchone()
         connection.close()
         
         max_score_value = max_score['SUM(score)']
         
         return max_score_value


def verify_if_game_id_exists(quiz: Quiz = None, game_id: int = None):
    
    connection, cursor = connect_database()
    
    if quiz:
        
        query = f"""
        SELECT g.id FROM Quiz q
        left join Game g on g.id = q.game_id 
        WHERE g.id = {quiz.game_id}
        ;
        """
    
    if game_id:
        
        query = f"""
        SELECT g.id FROM Quiz q
        left join Game g on g.id = q.game_id 
        WHERE g.id = {game_id}  
        ;
        """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        game_id_exists = cursor.fetchone()
        connection.close()

        return game_id_exists
    
     
def verify_if_quiz_id_exists(company_id: int, quiz: Quiz = None, quiz_id: int = None):
    
    connection, cursor = connect_database()
    
    if quiz:

        query = f"""
        SELECT id FROM Quiz
        WHERE id = {quiz.quiz_id};
        """
    
    if quiz_id and company_id:

        query = f"""
        SELECT q.id FROM Quiz q  
        RIGHT JOIN Game g ON g.id = q.game_id 
        RIGHT JOIN GamifiedJourney gj  ON gj.id = g.gamified_journey_id 
        RIGHT JOIN Company c ON c.id = gj.company_id 
        WHERE q.id = {quiz_id} and c.id = {company_id}
        ;
        """
    
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        quiz_id_exists = cursor.fetchone()
        connection.close()

        return quiz_id_exists
    
    
def verify_if_alternative_id_exists(alternative_list: list, quiz_id: int):
    
    connection, cursor = connect_database()

    placeholder = ','.join(['%s'] * len(alternative_list))

    query = f"""
    SELECT id
    FROM Alternative 
    WHERE id IN ({placeholder}) AND quiz_id = %s
    ;
    """

    try:
        cursor.execute(query, alternative_list + [quiz_id])

    except Exception as error:
        connection.close()
        return []

    else:
        
        alternative_id_exists = cursor.fetchall()
        connection.close()
        
        return alternative_id_exists