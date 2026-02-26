CREATE DATABASE IF NOT EXISTS gestorIA;
USE gestorIA;

-- ============================================
-- USERS TABLE (new - multi-user support)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(255) NOT NULL UNIQUE,
    PASSWORD_HASH VARCHAR(255) NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- CATEGORIES TABLE (updated - user-scoped)
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT,
    NAME VARCHAR(100) NOT NULL,
    CONSTRAINT FK_CATEGORY_USER FOREIGN KEY (USER_ID) REFERENCES users(ID) ON DELETE CASCADE
);

-- ============================================
-- EXPENSES TABLE (updated - user-scoped)
-- ============================================
CREATE TABLE IF NOT EXISTS expenses (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL,
    CATEGORY INT,
    TYPE ENUM('plm', 'manual', 'ocr'),
    MOVEMENT ENUM('Income', 'Expense', 'Savings'),
    NAME VARCHAR(100) NOT NULL,
    AMOUNT DECIMAL(10,2) NOT NULL,
    DATE DATE NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_CATEGORY FOREIGN KEY (CATEGORY) REFERENCES categories(ID),
    CONSTRAINT FK_EXPENSE_USER FOREIGN KEY (USER_ID) REFERENCES users(ID) ON DELETE CASCADE
);

-- ============================================
-- USER PROCEDURES
-- ============================================

DELIMITER //
CREATE PROCEDURE createUser(IN p_name VARCHAR(100), IN p_email VARCHAR(255), IN p_password_hash VARCHAR(255))
BEGIN
    INSERT INTO users(NAME, EMAIL, PASSWORD_HASH) VALUES(p_name, p_email, p_password_hash);
    SELECT ID, NAME, EMAIL, CREATED_AT FROM users WHERE ID = LAST_INSERT_ID();
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getUserByEmail(IN p_email VARCHAR(255))
BEGIN
    SELECT * FROM users WHERE EMAIL = p_email;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getUserById(IN p_id INT)
BEGIN
    SELECT ID, NAME, EMAIL, CREATED_AT FROM users WHERE ID = p_id;
END //
DELIMITER ;

-- ============================================
-- CATEGORY PROCEDURES (updated for user scope)
-- ============================================

DELIMITER //
CREATE PROCEDURE addCategory(IN p_user_id INT, IN p_name VARCHAR(100))
BEGIN
    INSERT INTO categories(USER_ID, NAME) VALUES(p_user_id, p_name);
    SELECT * FROM categories WHERE ID = LAST_INSERT_ID();
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateCategory(IN p_id INT, IN p_name VARCHAR(100))
BEGIN
    UPDATE categories
    SET NAME = p_name
    WHERE ID = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getCategories(IN p_ID INT)
BEGIN
    SELECT * FROM categories WHERE ID = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetCategoryNames(IN p_user_id INT)
BEGIN
    SELECT * FROM categories WHERE USER_ID = p_user_id OR USER_ID IS NULL;
END //
DELIMITER ;

-- ============================================
-- EXPENSE PROCEDURES (updated for user scope)
-- ============================================

DELIMITER //
CREATE PROCEDURE addExpense(
    IN p_user_id INT,
    IN p_category INT,
    IN p_type ENUM('plm', 'manual', 'ocr'),
    IN p_movement ENUM('income', 'expense', 'savings'),
    IN p_name VARCHAR(100),
    IN p_amount DECIMAL(10,2),
    IN p_date DATE
)
BEGIN
    INSERT INTO expenses(USER_ID, CATEGORY, TYPE, MOVEMENT, NAME, AMOUNT, DATE)
    VALUES(p_user_id, p_category, p_type, p_movement, p_name, p_amount, p_date);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateExpense(
    IN p_id INT,
    IN p_user_id INT,
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
    WHERE ID = p_id AND USER_ID = p_user_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteExpense(IN p_id INT, IN p_user_id INT)
BEGIN
    DELETE FROM expenses WHERE ID = p_id AND USER_ID = p_user_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpenses(IN p_user_id INT)
BEGIN
    SELECT * FROM expenses WHERE USER_ID = p_user_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesId(IN p_ID INT, IN p_user_id INT)
BEGIN
    SELECT * FROM expenses WHERE ID = p_ID AND USER_ID = p_user_id;
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
CREATE PROCEDURE get5Expenses(IN p_user_id INT)
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
    WHERE e.USER_ID = p_user_id
    ORDER BY e.CREATED_AT DESC
    LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getTopCategories(IN p_user_id INT)
BEGIN
    SELECT
        c.NAME AS CATEGORY_NAME,
        SUM(e.AMOUNT) AS TOTAL_AMOUNT
    FROM expenses e
    JOIN categories c ON e.CATEGORY = c.ID
    WHERE e.USER_ID = p_user_id
    GROUP BY c.NAME
    ORDER BY TOTAL_AMOUNT DESC
    LIMIT 5;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getTotalByMovement(IN p_user_id INT, IN p_movement VARCHAR(20))
BEGIN
    SELECT
        p_movement AS MOVEMENT_TYPE,
        COALESCE(SUM(AMOUNT), 0) AS TOTAL_AMOUNT
    FROM expenses
    WHERE USER_ID = p_user_id AND MOVEMENT = p_movement;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByTypeOPM(IN p_user_id INT, IN p_type VARCHAR(10))
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
    WHERE e.USER_ID = p_user_id AND e.TYPE = p_type
    ORDER BY e.DATE DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByCategory(IN p_user_id INT, IN p_category_id INT)
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
    WHERE e.USER_ID = p_user_id AND e.CATEGORY = p_category_id
    ORDER BY e.DATE DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByMonthRange(IN p_user_id INT, IN p_start_month INT, IN p_end_month INT)
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
    WHERE e.USER_ID = p_user_id AND MONTH(e.DATE) BETWEEN p_start_month AND p_end_month
    ORDER BY e.DATE DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getExpensesByAmountRange(IN p_user_id INT, IN p_min DECIMAL(10,2), IN p_max DECIMAL(10,2))
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
    WHERE e.USER_ID = p_user_id AND e.AMOUNT BETWEEN p_min AND p_max
    ORDER BY e.AMOUNT DESC;
END //
DELIMITER ;
