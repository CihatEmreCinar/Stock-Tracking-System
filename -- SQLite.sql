-- SQLite
ALTER TABLE Product ADD COLUMN weight REAL;
ALTER TABLE Sale ADD COLUMN vat_amount REAL;
.schema Product
.schema Sale
