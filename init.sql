-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vector similarity search functions
CREATE OR REPLACE FUNCTION cosine_similarity(a vector, b vector)
RETURNS float
LANGUAGE plpgsql
IMMUTABLE STRICT PARALLEL SAFE
AS $$
BEGIN
    RETURN 1 - (a <=> b);
END;
$$;
