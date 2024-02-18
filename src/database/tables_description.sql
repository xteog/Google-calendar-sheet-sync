CREATE TABLE Schedule (
    start DATETIME PRIMARY KEY,
    end DATETIME NOT NULL,
    equipment TEXT
);

CREATE TABLE Users(
    email varchar(64) PRIMARY KEY,
    name varchar(64) UNIQUE
);

CREATE TABLE TrainingType (
    date DATE NOT NULL,
    user VARCHAR(255) NOT NULL,
    type ENUM('Dinamica', 'Statica') DEFAULT 'Dinamica',
    priority INT,
    lock BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(date, user),
    FOREIGN KEY(date) REFERENCES Schedule (start) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user) REFERENCES Users (email) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Events (
    id varchar(64) PRIMARY KEY,
    start DATETIME NOT NULL,
    attendee varchar(64) NOT NULL,
    title varchar(64) NOT NULL,
    description TEXT NOT NULL,
    response ENUM(
        "accepted",
        "declined",
        "tentative",
        "needsAction"
    ) NOT NULL,
    FOREIGN KEY (start) REFERENCES Schedule (start) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (attendee) REFERENCES Users (email) ON UPDATE CASCADE ON DELETE CASCADE
);