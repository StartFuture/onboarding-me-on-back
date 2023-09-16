SELECT * FROM Company c;

SELECT * FROM Chat c;
SELECT * FROM Chat_Employee ce;
SELECT * FROM Message m;

SELECT * FROM Employee e;
SELECT * FROM Employee_Alternative ea;
SELECT * FROM Employee_Tool et;

SELECT * FROM Address a ;

SELECT * FROM Tracking t;
SELECT * FROM WelcomeKit wk;
SELECT * FROM WelcomeKit_WelcomeKitItem wkwki;
SELECT * FROM WelcomeKitItem wki;


SELECT * FROM GamifiedJourney gj ;
SELECT * FROM Game g ;
SELECT * FROM Quiz q ;
SELECT * FROM Alternative a;

SELECT * FROM Tool t;
SELECT * FROM CategoryTool ct;

SELECT * FROM Medal m;
SELECT * FROM Medal_Score ms ;
SELECT * FROM Score s;


INSERT INTO Company
(company_name, trading_name, cnpj, email, company_password, state_register)
VALUES('Google', 'Google', '123.456', 'teste@gmail.com', '123', 'SP');

INSERT INTO onboarding_me.Address
(num, complement, zipcode, street, district, city, state)
VALUES('string', 'string', 'string', 'string', 'string', 'string', 'string');

INSERT INTO onboarding_me.Employee
(first_name, surname, birthdate, employee_role, email, employee_password, phone_number, cpf, level_access, company_id, address_id)
VALUES('string', 'string', '1000-01-01', 'string', 'string.com', '123', '11111-1111', '123.123', 'default', 1, 1);

INSERT INTO onboarding_me.Chat
(company_id, first_employee_id)
VALUES(1, 1);

INSERT INTO onboarding_me.Message
(user_to, user_from, message, created_date, read_date, chat_id)
VALUES(1, 1, 'string', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);

INSERT INTO onboarding_me.Chat_Employee
(chat_id, second_employee_id)
VALUES(1, 1);

INSERT INTO onboarding_me.WelcomeKit
(name)
VALUES('string');

INSERT INTO onboarding_me.Tracking
(tracking_code, status, employee_id, welcome_kit_id)
VALUES('string', 'sended', 1, 1);

ALTER TABLE WelcomeKitItem MODIFY image blob NULL;

INSERT INTO onboarding_me.WelcomeKitItem
(name)
VALUES('string');

INSERT INTO onboarding_me.WelcomeKit_WelcomeKitItem
(welcome_kit_id, item_id)
VALUES(1, 1);

INSERT INTO GamifiedJourney
(welcome_video_link, company_id)
VALUES('string', 1);

INSERT INTO onboarding_me.Game
(name, gamified_journey_id)
VALUES('super-name', 1);

INSERT INTO onboarding_me.Quiz
(link_video, score, title, question, quiz_type, game_id)
VALUES('string', 0, 'string', 'string', 'culture', 1);

INSERT INTO onboarding_me.Alternative
(alternative_text, is_answer, quiz_id)
VALUES('string', 0, 1);

INSERT INTO onboarding_me.CategoryTool
(name)
VALUES('string');

INSERT INTO onboarding_me.Tool
(link_download, score, name, game_id, category_id)
VALUES('string', 1, 'string', 1, 1);

INSERT INTO onboarding_me.Employee_Tool
(employee_id, tool_id, nick_name)
VALUES(1, 1, 'string');

INSERT INTO onboarding_me.Employee_Alternative
(employee_id, alternative_id)
VALUES(1, 1);

INSERT INTO onboarding_me.Employee_Feedback
(employee_id, grade, message, feedback_type)
VALUES(1, 1, 'string', 'welcomekit');

INSERT INTO onboarding_me.Score
(total_points, last_updated, employee_id, game_id)
VALUES(0, '2023-08-01 00:00:00', 1, 1);

ALTER TABLE Medal MODIFY image blob NULL;

INSERT INTO onboarding_me.Medal
(name, game_id)
VALUES('string',  1);

INSERT INTO onboarding_me.Medal_Score
(medal_id, score_id)
VALUES(1, 1);
