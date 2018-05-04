/*
  Evan James
  MySQL script to create sample views to export data to test the vis on a smaller dataset
*/
ALTER TABLE Songs ADD ArtistName char(128);
UPDATE Songs A SET ArtistName = (SELECT Name FROM Artists B WHERE A.Artist = B.ID);

/*
CREATE OR REPLACE VIEW SampleExportRel AS SELECT * FROM Rel LIMIT 25;

CREATE OR REPLACE VIEW SampleExportDillaSongs AS
  SELECT * FROM Songs WHERE ID IN
    (SELECT Song FROM SampleExportRel);

CREATE OR REPLACE VIEW SampleExportSampledSongs AS
  SELECT * FROM Songs WHERE ID IN
    (SELECT Sampled FROM SampleExportRel);
*/

CREATE OR REPLACE VIEW ExportRels AS
  SELECT * FROM Rel LIMIT 500;

CREATE OR REPLACE VIEW ExportDillaSongs AS
  SELECT * FROM Songs WHERE ID IN (SELECT Song FROM ExportRels);

CREATE OR REPLACE VIEW ExportSampledSongs AS
  SELECT * FROM Songs WHERE ID IN (SELECT Sampled FROM ExportRels);
