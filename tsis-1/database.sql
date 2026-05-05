CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
   name VARCHAR,
   email VARCHAR,
   phone VARCHAR,
   type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
   RETURN QUERY
   SELECT
       c.name,
       c.email,
       p.phone,
       p.type
   FROM contacts c
   LEFT JOIN phones p ON c.id = p.contact_id
   WHERE
       c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;