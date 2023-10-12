DROP TABLE IF EXISTS contestQuestions;
CREATE TABLE "contestQuestions" (
	"id"	INTEGER,
	"date"	TEXT,
	"questionNum"	INTEGER DEFAULT 1,
	"refAnswer"	TEXT,
	"userId"	INTEGER,
	"userName"	TEXT,
	"settingTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"availableTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"deactivatingTime"	TIMESTAMP NOT NULL DEFAULT '2050-12-31 23:59:59',
	PRIMARY KEY("id" AUTOINCREMENT)
)
DROP TABLE IF EXISTS contestUserAnswers;
CREATE TABLE "contestUserAnswers" (
	"id"	INTEGER,
	"date"	TEXT,
	"questionNum"	INTEGER,
	"answer"	TEXT,
	"userId"	INTEGER,
	"userName"	TEXT,
	"submittingTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"correction"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
DROP TABLE IF EXISTS contestUserLog;
CREATE TABLE "contestUserLog" (
	"id"	INTEGER,
	"userId"	INTEGER,
	"userName"	TEXT,
	"contestDate"	TEXT,
	"startTime"	TEXT,
	"endTime"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
DROP TABLE IF EXISTS contests;
CREATE TABLE "contests" (
	"id"	INTEGER DEFAULT 1,
	"date"	TEXT,
	"notes"	TEXT,
	"availableDate"	TEXT,
	"deactivatingDate"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
DROP TABLE IF EXISTS dailyQuestions;
CREATE TABLE "dailyQuestions" (
	"id"	INTEGER,
	"date"	TEXT,
	"questionNum"	INTEGER DEFAULT 1,
	"refAnswer"	TEXT,
	"userId"	INTEGER,
	"userName"	TEXT,
	"settingTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"availableTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"deactivatingTime"	TIMESTAMP NOT NULL DEFAULT '2050-12-31 23:59:59',
	PRIMARY KEY("id" AUTOINCREMENT)
)
DROP TABLE IF EXISTS dailyUserAnswers;
CREATE TABLE "dailyUserAnswers" (
	"id"	INTEGER,
	"date"	TEXT,
	"questionNum"	INTEGER,
	"answer"	TEXT,
	"userId"	INTEGER,
	"userName"	TEXT,
	"submittingTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"correction"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
DROP TABLE IF EXISTS users;
CREATE TABLE "users" (
	"id"	INTEGER,
	"userName"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"email"	TEXT,
	"group"	TEXT DEFAULT 'members',
	"registeringTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
	"deactivatingTime"	TIMESTAMP NOT NULL DEFAULT '2050-12-31 23:00:00',
	PRIMARY KEY("id" AUTOINCREMENT)
)
