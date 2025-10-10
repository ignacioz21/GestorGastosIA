CREATE DATABASE gestorIA;
USE gestorIA;

CREATE TABLE IF NOT EXISTS categories (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    CATEGORY INT,
    TYPE ENUM('plm', 'manual', 'ocr'),
    MOVEMENT ENUM('Income', 'Expense', 'Savings'),
    NAME VARCHAR(100) NOT NULL,
    AMOUNT DECIMAL NOT NULL,
    DATE DATE NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_CATEGORY FOREIGN KEY (CATEGORY) REFERENCES categories(ID)
);

DELIMITER //
CREATE PROCEDURE addCategory(IN p_name VARCHAR(100))
BEGIN
	INSERT INTO categories(NAME) VALUES(p_name);
    SELECT * FROM categories WHERE NAME = p_name;
END //
DELIMITER;

DELIMITER //
CREATE PROCEDURE updateCategory(IN p_id INT, IN p_name VARCHAR(100))
BEGIN
	UPDATE categories
    SET NAME = p_name
    WHERE ID = P_id;
END //
DELIMITER;

DELIMITER //
CREATE PROCEDURE getCategories(IN p_ID INT)
BEGIN
	SELECT * FROM categories WHERE ID = p_id;
END //
DELIMITER;

DELIMITER //
CREATE PROCEDURE GetCategoryNames()
BEGIN
    SELECT * FROM categories;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE addExpense(
	IN p_category INT,
    IN p_type ENUM('plm', 'manual', 'ocr'),
    IN p_movement ENUM('income', 'expense', 'savings'),
    IN p_name VARCHAR(100),
    IN p_amount DECIMAL(10,2),
    IN p_date DATE
)
BEGIN
	INSERT INTO expenses(CATEGORY, TYPE, MOVEMENT, NAME, AMOUNT, DATE)
    VALUES(p_category, p_type, p_movement, p_name, p_amount, p_date);
END // 
DELIMITER;

DELIMITER // 
CREATE PROCEDURE updateExpense(
	IN p_id INT,
    IN p_category INT,
    IN p_type ENUM('plm', 'manual', 'ocr'),
    IN p_movement ENUM('income', 'expense', 'savings'),
    IN p_name VARCHAR(100),
    IN p_amount DECIMAL(10,2),
    IN p_date DATE
)
BEGIN
	UPDATE expenses
    SET CATEGORY = p_category,
        TYPE = p_type,
        MOVEMENT = p_movement,
        NAME = p_name,
        AMOUNT = p_amount,
        DATE = p_date
    WHERE ID = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpenses()
BEGIN
	SELECT * FROM expenses;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesId(IN p_ID INT)
BEGIN
	SELECT * FROM expenses WHERE ID = p_ID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getEnums(IN p_column_name VARCHAR(100))
BEGIN
	SELECT COLUMN_TYPE
	FROM information_schema.COLUMNS
	WHERE TABLE_SCHEMA = DATABASE()
	  AND TABLE_NAME = 'expenses'
	  AND COLUMN_NAME = p_column_name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get5Expenses()
BEGIN
    SELECT 
        e.ID,
        c.NAME AS CATEGORY_NAME,
        e.TYPE,
        e.MOVEMENT,
        e.NAME,
        e.AMOUNT,
        e.DATE,
        e.CREATED_AT
    FROM expenses e
    JOIN categories c ON e.CATEGORY = c.ID
    LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getTopCategories()
BEGIN
    SELECT 
        c.NAME AS CATEGORY_NAME,
        SUM(e.AMOUNT) AS TOTAL_AMOUNT
    FROM expenses e
    JOIN categories c ON e.CATEGORY = c.ID
    GROUP BY c.NAME
    ORDER BY TOTAL_AMOUNT DESC
    LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getTotalByMovement(IN p_movement VARCHAR(20))
BEGIN
    SELECT 
        p_movement AS MOVEMENT_TYPE,
        SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM expenses
    WHERE MOVEMENT = p_movement;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByTypeOPM(IN p_type VARCHAR(10))
BEGIN
	SELECT e.ID,
		   e.NAME,
		   e.AMOUNT,
		   e.DATE,
		   e.MOVEMENT,
		   e.TYPE,
		   c.NAME AS CATEGORY_NAME
	FROM expenses e
	JOIN categories c ON e.CATEGORY = c.ID
	WHERE e.TYPE = p_type
	ORDER BY e.DATE DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByCategory(IN p_category_id INT)
BEGIN
	SELECT e.ID,
		   e.NAME,
		   e.AMOUNT,
		   e.DATE,
		   e.MOVEMENT,
		   e.TYPE,
		   c.NAME AS CATEGORY_NAME
	FROM expenses e
	JOIN categories c ON e.CATEGORY = c.ID
	WHERE e.CATEGORY = p_category_id
	ORDER BY e.DATE DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByMonthRange(IN p_start_month INT, IN p_end_month INT)
BEGIN
	SELECT e.ID,
		   e.NAME,
		   e.AMOUNT,
		   e.DATE,
		   e.MOVEMENT,
		   e.TYPE,
		   c.NAME AS CATEGORY_NAME
	FROM expenses e
	JOIN categories c ON e.CATEGORY = c.ID
	WHERE MONTH(e.DATE) BETWEEN p_start_month AND p_end_month
	ORDER BY e.DATE DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByAmountRange(IN p_min DECIMAL(10,2), IN p_max DECIMAL(10,2))
BEGIN
	SELECT e.ID,
		   e.NAME,
		   e.AMOUNT,
		   e.DATE,
		   e.MOVEMENT,
		   e.TYPE,
		   c.NAME AS CATEGORY_NAME
	FROM expenses e
	JOIN categories c ON e.CATEGORY = c.ID
	WHERE e.AMOUNT BETWEEN p_min AND p_max
	ORDER BY e.AMOUNT DESC;
END //
DELIMITER ;



CALL getEnums('TYPE');
CALL GetCategoryNames();
CALL get5Expenses();
CALL getTopCategories();
CALL getTotalByMovement("expense");

CALL getExpensesByTypeOPM('ocr');
CALL getExpensesByTypeOPM('plm');
CALL getExpensesByTypeOPM('manual');

CALL getExpensesByCategory(1);

CALL getExpensesByMonthRange(9, 10); 

CALL getExpensesByAmountRange(10, 15); 


SELECT * FROM categories;
SELECT * FROM expenses;
DROP TABLE categories;

INSERT INTO categories(NAME) VALUES("comida");