from app.dao.dao import connect_database
from app.schemas.quiz import Quiz, Alternative


def select_quiz(id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT q.title, q.score  FROM Quiz q
    left join Game g on g.id = q.game_id 
    left join GamifiedJourney gj on gj.id = g.gamified_journey_id 
    left join Company c on c.id = gj.company_id 
    WHERE
    c.id = {id}
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
        
        cursor.execute(query)
        
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



def verify_if_game_id_exists(quiz: Quiz):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT g.id FROM Quiz q
    left join Game g on g.id = q.game_id 
    WHERE g.id = {quiz.game_id}
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
    
    
    
def verify_if_quiz_id_exists(quiz: Quiz):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id FROM Quiz
    WHERE id = {quiz.quiz_id};
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
    WHERE id IN ({placeholder}) AND quiz_id = %s;
    """

    try:
        cursor.execute(query, alternative_list + [quiz_id])
        alternative_id_exists = cursor.fetchall()

    except Exception as error:
        connection.close()
        return []

    else:
        connection.close()
        return alternative_id_exists