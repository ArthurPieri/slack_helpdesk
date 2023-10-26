CREATE DATABASE mydatabase;

\c mydatabase;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.tickets (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    end_date TIMESTAMP,
    start_date TIMESTAMP NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    metadata JSONB
);
