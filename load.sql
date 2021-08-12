-- Use PostgresSQL to load a CSV file to the database

-- COMMANDS
SELECT * FROM "kanji"."kanji_list";

DELETE FROM "kanji"."kanji_list";

ALTER SEQUENCE "kanji"."kanji_list_id_seq" RESTART;

-- LOADER
COPY kanji.kanji_list(char, strokes, grade, freq, jlpt, wk)
FROM '/tmp/kanji.csv'
DELIMITER ','
CSV HEADER
NULL AS 'None';
