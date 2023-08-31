SELECT * FROM Company c;
SELECT * FROM GamifiedJourney gj ;
SELECT * FROM Game g;
SELECT * FROM Quiz q;
SELECT * FROM Alternative a;
SELECT * FROM CategoryTool ct;
SELECT * FROM Tool t;
SELECT * FROM Employee e;
SELECT * FROM Employee_Tool et ;
SELECT * FROM Score s ;
SELECT * FROM Medal m ;
SELECT * FROM Medal_Score ms ;

SELECT t.score FROM Employee_Tool et LEFT JOIN
Tool t ON t.id = et.tool_id;

INSERT INTO Company
(company_name, trading_name, cnpj, email, company_password, state_register)
VALUES('Google', 'Google', '123.456', 'teste@gmail.com', '123', 'SP');

INSERT INTO GamifiedJourney
(welcome_video_link, company_id)
VALUES('fds', 1);

INSERT INTO onboarding_me.Game
(name, gamified_journey_id)
VALUES('super-name', 1);

INSERT INTO onboarding_me.Quiz
(link_video, score, title, question, quiz_type, game_id)
VALUES('fds', 0, 'fds', 'fds', 'culture', 1);

INSERT INTO onboarding_me.Alternative
(alternative_text, is_answer, quiz_id)
VALUES('fds', 0, 1);

INSERT INTO onboarding_me.CategoryTool
(name)
VALUES('fds');

INSERT INTO onboarding_me.Tool
(link_download, score, name, game_id, category_id)
VALUES('fds', 1, 'fds', 1, 1);


INSERT INTO onboarding_me.Address
(num, complement, zipcode, street, district, city, state)
VALUES('fds', 'fds', 'fds', 'fds', 'fds', 'fds', 'fds');


INSERT INTO onboarding_me.Employee
(first_name, surname, birthdate, employee_role, email, employee_password, phone_number, cpf, level_access, company_id, address_id)
VALUES('fds', 'fds', '1000-01-01', 'fds', 'fds.com', '123', '11111-1111', '123.123', 'default', 1, 1);

INSERT INTO onboarding_me.Score
(total_points, last_updated, employee_id)
VALUES(100, CURRENT_TIMESTAMP, 1);

INSERT INTO onboarding_me.Medal
(name, image, game_id)
VALUES('ouro', '', 1);

INSERT INTO onboarding_me.Medal_Score
(medal_id, score_id)
VALUES(1, 1);