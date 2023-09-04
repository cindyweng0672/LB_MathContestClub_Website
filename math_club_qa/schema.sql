DROP TABLE IF EXISTS users;
CREATE TABLE "users" (
	"id"	INTEGER,
	"userName"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"email"		TEXT,
	"userGroup"	TEXT DEFAULT 'members',
	"registeringTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	"deactivatingTime"	TIMESTAMP NOT NULL DEFAULT '2050-12-31 23:00:00',
	PRIMARY KEY("id" AUTOINCREMENT)
);

DROP TABLE IF EXISTS questions;
CREATE TABLE "questions" (
	"id"	INTEGER,
	"dateFor"	TEXT,
	"refAnswer"	TEXT,
	"setterId", INTEGER,
	"setterName"	TEXT,
	"settingTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	"availableTime"	TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
	"deactivatingTime"	TIMESTAMP NOT NULL DEFAULT '2050-12-31 23:59:59',
	PRIMARY KEY("id" AUTOINCREMENT)
);

DROP TABLE IF EXISTS userAnswers;
CREATE TABLE "userAnswers" (
	"id"	INTEGER,
	"dateFor"	TEXT,
	"answer"	TEXT,
	"adderId"	INTEGER,
	"adderName"	TEXT,
	"submittingTime" TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  "correction" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

