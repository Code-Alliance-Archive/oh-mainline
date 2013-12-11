CREATE FUNCTION delete_from_zoho() RETURNS trigger AS '
BEGIN
    INSERT INTO profile_people_to_remove_from_zoho (zoho_id) VALUES (old.zoho_id);
END
' LANGUAGE plpgsql;

CREATE TRIGGER delete_from_zoho_trigger AFTER DELETE ON profile_person FOR EACH ROW
  EXECUTE PROCEDURE delete_from_zoho();
