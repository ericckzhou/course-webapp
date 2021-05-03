CREATE TABLE IF NOT EXISTS Users (
	'uid' INTEGER NOT NULL PRIMARY KEY,
	username NVARCHAR(50) NOT NULL,
	password NVARCHAR(50) NOT NULL,
	'type' NVARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS Students (
	sid INTEGER NOT NULL PRIMARY KEY,
	username NVARCHAR(50) NOT NULL,
	fname NVARCHAR(30) NOT NULL,
	lname NVARCHAR(30) NOT NULL,
	q1 INTEGER NOT NULL,
	q2 INTEGER NOT NULL,
	q3 INTEGER NOT NULL,
	q4 INTEGER NOT NULL,
	a1 INTEGER NOT NULL,
	a2 INTEGER NOT NULL,
	a3 INTEGER NOT NULL,
	final INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS Instructors (
	id INTEGER NOT NULL PRIMARY KEY,
	username NVARCHAR(50) NOT NULL,
	fname NVARCHAR(30) NOT NULL,
	lname NVARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS Feedback (
	fid INTEGER NOT NULL PRIMARY KEY,
	username NVARCHAR(50) NOT NULL,
	ans1 NVARCHAR(100) NOT NULL,
	ans2 NVARCHAR(100) NOT NULL,
	ans3 NVARCHAR(100) NOT NULL,
	ans4 NVARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS Remarks (
	rid INTEGER NOT NULL PRIMARY KEY,
	username NVARCHAR(50) NOT NULL,
	what NVARCHAR(30) NOT NULL,
	why NVARCHAR(100) NOT NULL,
	status NVARCHAR(10) NOT NULL
);

INSERT INTO Users VALUES (1, "eric", "zhou", "student");
INSERT INTO Users VALUES (2, "zhaoyue", "yang", "student");
INSERT INTO Users VALUES (3, "shijun", "sui", "student");
INSERT INTO Users VALUES (4, "abbas_a", "a", "instructor");
INSERT INTO Users VALUES (5, "purva_g", "g", "instructor");
INSERT INTO Users VALUES (6, "student1", "student1", "student");
INSERT INTO Users VALUES (7, "student2", "student2", "student");
INSERT INTO Users VALUES (8, "instructor1", "instructor1", "instructor");
INSERT INTO Users VALUES (9, "instructor2", "instructor2", "instructor");

INSERT INTO Students VALUES (1, "eric", "eric", "zhou", 1, 1, 1, 1, 1, 1, 1, 1);
INSERT INTO Students VALUES (2, "zhaoyue", "zhaoyue", "yang", 2, 2, 2, 2, 2, 2, 2, 2);
INSERT INTO Students VALUES (3, "shijun", "shijun", "sui", 3,3,3,3,3,3,3,3);
INSERT INTO Students VALUES (4, "student1", "student1", "student1", 70, 75, 80, 85, 70, 80, 90, 65);
INSERT INTO Students VALUES (5, "student2", "student2", "student2", 100, 95, 90, 85, 90, 92, 94, 89);

INSERT INTO Instructors VALUES (1, "abbas_a", "abbas", "a");
INSERT INTO Instructors VALUES (2, "purva_g", "purva", "g");
INSERT INTO Instructors VALUES (3, "instructor1", "instructor1", "instructor1");
INSERT INTO Instructors VALUES (4, "instructor2", "instructor2", "instructor2");

INSERT INTO Feedback VALUES (1, "abbas_a", "Interactive", "More images", "Great at explaining", "Nothing! It's all good!");
INSERT INTO Feedback VALUES (2, "purva_g", "Great at explaining", "Talk slower!", "Colorful HTML", "Talk louder!");

INSERT INTO Remarks VALUES (1, "eric", "a3", "incorrect total","closed");
