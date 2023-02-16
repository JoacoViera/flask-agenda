CREATE TABLE users(
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL, 
    password VARCHAR(255) NOT NULL , PRIMARY KEY (user_id)
);

CREATE TABLE user_contacts (
    user_id INT NOT NULL,
    contact_id INT NOT NULL 
);

CREATE TABLE contacts (
    contact_id INT NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT NULL, PRIMARY KEY (contact_id)
);

SELECT c.fullname, c.phone, c.email
FROM contacts c LEFT JOIN user_contacts uc ON c.contact_id = uc.contact_id
LEFT JOIN users u ON uc.user_id = u.user_id;


INSERT INTO MyTable (MyField) 
VALUES (CAST(GETDATE() AS TIME))