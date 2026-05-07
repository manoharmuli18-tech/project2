# Flask Blog App

A simple blog application built with Flask and PostgreSQL.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (copy .env and update values)

3. Run the app:
   ```bash
   python app.py
   ```

## Vercel Deployment

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Set environment variables in Vercel dashboard:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: A secure random string

## Features

- User authentication
- Create, read, update, delete blog posts
- PostgreSQL database
- Bootstrap UI