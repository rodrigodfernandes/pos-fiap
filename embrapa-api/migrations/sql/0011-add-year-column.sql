-- 0011-add-column-year_no.sql
ALTER TABLE product ADD COLUMN year_no INT;
ALTER TABLE process ADD COLUMN year_no INT;
ALTER TABLE sales ADD COLUMN year_no INT;
ALTER TABLE import ADD COLUMN year_no INT;
ALTER TABLE export ADD COLUMN year_no INT;
