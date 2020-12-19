CREATE TABLE "global_state" (
	"id" serial NOT NULL,
	"key" varchar(255) NOT NULL UNIQUE,
	"value" TEXT NOT NULL,
	CONSTRAINT "global_state_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "secret_santa" (
	"id" serial NOT NULL,
	"season" integer NOT NULL,
	"participant" varchar(255) NOT NULL,
	"prompt" varchar(800) NOT NULL,
	"prompt_attachments" TEXT NOT NULL,
	"paired_id" integer NOT NULL,
	"gift" TEXT NOT NULL,
	"gift_revealed" BOOLEAN NOT NULL,
	CONSTRAINT "secret_santa_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "emotes" (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	"source" TEXT NOT NULL,
	CONSTRAINT "emotes_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);