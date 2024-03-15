-- Check if the schema and table exist, if not, create them
CREATE SCHEMA IF NOT EXISTS code_snippet;

CREATE TABLE IF NOT EXISTS code_snippet.llm_logger (
    response_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    query TEXT,
    response TEXT,
    snippets TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
