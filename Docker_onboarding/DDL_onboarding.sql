CREATE DATABASE IF NOT EXISTS onboarding_db DEFAULT CHARACTER SET utf8;
USE onboarding_db;

-- create a table Enterprise

CREATE TABLE IF NOT EXISTS Enterprise(
    id_enterprise INT NOT NULL AUTO_INCREMENT,
    fictitious_name VARCHAR(100) NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    state_registration VARCHAR(12) NOT NULL UNIQUE,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    logo BLOB,
    password_login VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY(id_enterprise)
);

-- create a table Addres

CREATE TABLE IF NOT EXISTS Address(
    id_address INT NOT NULL AUTO_INCREMENT,
    cep VARCHAR(9) NOT NULL,
    state VARCHAR(30) NOT NULL,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(100) NOT NULL,
    number INT NOT NULL,
    neighbourhood VARCHAR(50) NOT NULL,
    complement VARCHAR(100),
    PRIMARY KEY(id_address)
);

-- create a table Employee

CREATE TABLE IF NOT EXISTS Employee(
    id_employee INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    phone_number VARCHAR(14) NOT NULL,
    corporate_email VARCHAR(255) NOT NULL UNIQUE,
    birth_date DATE NOT NULL,
    job_position VARCHAR(100) NOT NULL,
    password_login VARCHAR(50) NOT NULL,
    PRIMARY KEY(id_employee),
    id_enterprise INT,
    id_address INT,
    FOREIGN KEY(id_enterprise) REFERENCES Enterprise(id_enterprise),
    FOREIGN KEY(id_address) REFERENCES Address(id_address)
);

-- create a table WelcomeKit

CREATE TABLE IF NOT EXISTS WelcomeKit(
    id_welcomekit INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    image BLOB NOT NULL,
    PRIMARY KEY(id_welcomekit)
);

-- create a table WelcomeKit_Item

CREATE TABLE IF NOT EXISTS WelcomeKit_Item(
    id_welcomekit_item INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    image BLOB NOT NULL,
    PRIMARY KEY(id_welcomekit_item)
);

-- create a table WelcomeKit_Connection

CREATE TABLE IF NOT EXISTS WelcomeKit_Connection(
    id INT NOT NULL AUTO_INCREMENT,
    id_welcomekit_item INT,
    id_welcomekit INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(id_welcomekit_item) REFERENCES WelcomeKit_Item(id_welcomekit_item),
    FOREIGN KEY(id_welcomekit) REFERENCES WelcomeKit(id_welcomekit)
);

-- create a table Tracking

CREATE TABLE IF NOT EXISTS Tracking(
    id_tracking INT NOT NULL AUTO_INCREMENT,
    tracking_num VARCHAR(13) NOT NULL,
    status_tracking ENUM('in-preparation', 'sended', 'delivered') NOT NULL,
    id_employee INT UNIQUE,
    id_welcomekit INT,
    PRIMARY KEY(id_tracking),
    FOREIGN KEY(id_employee) REFERENCES Employee(id_employee),
    FOREIGN KEY(id_welcomekit) REFERENCES WelcomeKit(id_welcomekit)
);

-- create a table Gamified_Journey

CREATE TABLE IF NOT EXISTS Gamified_Journey(
    id_gamified INT NOT NULL AUTO_INCREMENT,
    welcome_video_link VARCHAR(255) NOT NULL,
    id_enterprise INT UNIQUE,
    PRIMARY KEY(id_gamified),
    FOREIGN KEY(id_enterprise) REFERENCES Enterprise(id_enterprise)
);

-- create a table Game

CREATE TABLE IF NOT EXISTS Game(
    id_game INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    id_gamified INT,
    PRIMARY KEY(id_game),
    FOREIGN KEY(id_gamified) REFERENCES Gamified_Journey(id_gamified)
);

-- create a table Quiz

CREATE TABLE IF NOT EXISTS Quiz(
    id_quiz INT NOT NULL AUTO_INCREMENT,
    link_video VARCHAR(255) NOT NULL,
    type ENUM('culture', 'principles') NOT NULL,
    title VARCHAR(255) NOT NULL,
    question VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    game_id INT,
    PRIMARY KEY(id_quiz),
    FOREIGN KEY(game_id) REFERENCES Game(id_game)
);

-- create a table Alternative

CREATE TABLE IF NOT EXISTS Alternative(
    id_alternative INT NOT NULL AUTO_INCREMENT,
    is_answer TINYINT NOT NULL,
    answer VARCHAR(255) NOT NULL,
    quiz_id INT,
    PRIMARY KEY(id_alternative),
    FOREIGN KEY(quiz_id) REFERENCES Quiz(id_quiz)
);

-- create a table Alternative_Employee

CREATE TABLE IF NOT EXISTS Alternative_Employee(
    id INT NOT NULL AUTO_INCREMENT,
    id_alternative INT,
    id_employee INT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_alternative) REFERENCES Alternative(id_alternative),
    FOREIGN KEY(id_employee) REFERENCES Employee(id_employee)
);

-- create a table Category_Tool

CREATE TABLE IF NOT EXISTS Category_Tool(
    id_category_tool INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY(id_category_tool)
);

-- create a table Tool

CREATE TABLE IF NOT EXISTS Tool(
    id_tool INT NOT NULL AUTO_INCREMENT,
    name_tool VARCHAR(100) NOT NULL,
    link_download VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    category_tool_id INT,
    game_id INT,
    PRIMARY KEY(id_tool),
    FOREIGN KEY(category_tool_id) REFERENCES Category_Tool(id_category_tool),
    FOREIGN KEY(game_id) REFERENCES Game(id_game)
);

-- create a table Tool_Employee

CREATE TABLE IF NOT EXISTS Tool_Employee(
    id INT NOT NULL AUTO_INCREMENT,
    id_tool INT,
    id_employee INT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_tool) REFERENCES Tool(id_tool),
    FOREIGN KEY(id_employee) REFERENCES Employee(id_employee)
);

-- create a table Medals

CREATE TABLE IF NOT EXISTS Medals(
    id_medals INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    image BLOB NOT NULL,
    game_id INT,
    PRIMARY KEY(id_medals),
    FOREIGN KEY(game_id) REFERENCES Game(id_game)
);

-- create a table Score

CREATE TABLE IF NOT EXISTS Score(
    id_score INT NOT NULL AUTO_INCREMENT,
    total_points INT NOT NULL,
    last_updated INT NOT NULL,
    id_employee INT UNIQUE,
    PRIMARY KEY(id_score),
    FOREIGN KEY(id_employee) REFERENCES Employee(id_employee)
);

-- create a table Medals_Score

CREATE TABLE IF NOT EXISTS Medals_Score(
    id INT NOT NULL AUTO_INCREMENT,
    id_medals INT,
    id_score INT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_medals) REFERENCES Medals(id_medals),
    FOREIGN KEY(id_score) REFERENCES Score(id_score)
);
