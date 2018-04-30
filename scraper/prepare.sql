/*
  Evan James
  MySQL script to create sample views to export data to test the vis on a smaller dataset
*/
CREATE OR REPLACE VIEW SampleExportRel AS SELECT * FROM Rel LIMIT 25;

CREATE OR REPLACE VIEW SampleExportSongs AS
  SELECT * FROM Songs WHERE ID IN
    (SELECT Song FROM SampleExportRel)
  UNION
  SELECT * FROM Songs WHERE ID IN
    (SELECT Sampled FROM SampleExportRel);

CREATE OR REPLACE VIEW SampleExportArtists AS SELECT * FROM Artists WHERE ID IN
    (SELECT Artist FROM SampleExportSongs);