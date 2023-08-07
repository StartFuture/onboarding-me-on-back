from app.dao.dao import connect_database
from app.schemas.quiz import Quiz
from app.schemas.alternative import Alternative

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


def insert_quiz(quiz: Quiz):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO Quiz 
    (link_video, score, title, question, quiz_type, game_id)
    VALUES
    ('{quiz.link_video}', '{quiz.score}', '{quiz.title}', '{quiz.question}', '{quiz.quiz_type}', '1');
    """

    cursor.execute(query)
    connection.commit()

    query = f'SELECT title FROM Quiz WHERE title = "{quiz.title}"'

    cursor.execute(query)
    quiz_result = cursor.fetchone()
    connection.close()

    return quiz_result


def insert_alternative(alternative: Alternative):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO Alternative 
    (alternative_text, is_answer, quiz_id)
    VALUES
    ('{alternative.text}', '{alternative.is_answer}', '2');
    """

    cursor.execute(query)
    connection.commit()
    
    query = f'SELECT alternative_text FROM Alternative WHERE alternative_text = "{alternative.text}"'

    cursor.execute(query)
    alternative_result = cursor.fetchone()
    connection.close()

    return alternative_result


def update_quiz(quiz: Quiz):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE Quiz 
    SET 
    link_video = '{quiz.link_video}', score = '{quiz.score}', title = '{quiz.title}', question = '{quiz.question}', quiz_type = '{quiz.quiz_type}'
    WHERE id = 4;
    """

    cursor.execute(query)
    connection.commit()
 
    query = f'SELECT title FROM Quiz WHERE title = "{quiz.title}"'
 
    cursor.execute(query)
    quiz_result = cursor.fetchone()
    connection.close()
 
    return quiz_result


def update_alternative(alternative: Alternative):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE Alternative  
    SET alternative_text  = '{alternative.text}', is_answer  = {alternative.is_answer}
    WHERE id = 1;
    """

    cursor.execute(query)
    connection.commit()
    
    query = f'SELECT alternative_text FROM Alternative WHERE alternative_text = "{alternative.text}"'

    cursor.execute(query)
    alternative_result = cursor.fetchone()
    connection.close()

    return alternative_result