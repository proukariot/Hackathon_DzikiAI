# How to Run the Server with Docker

This guide explains how to build and run the FastAPI server inside
Docker.

------------------------------------------------------------------------

## \## 1. Make sure your project structure looks like this

    project/
    ├── Dockerfile
    ├── requirements.txt
    ├── .env
    ├── llm/
    │   └── server.py
    └── ...

------------------------------------------------------------------------

## \## 2. Create a `.env` file

Example dummy `.env`:

    OPENAI_API_KEY=sk-test-123456
    MODEL=gpt-4.1
    SUPABASE_URL=https://dummy-project.supabase.co
    SUPABASE_KEY=dummy-service-role-key-123

Put this file next to `Dockerfile`.

------------------------------------------------------------------------

## \## 3. Build Docker image

Run in terminal inside project folder:

``` bash
docker build -t pet-extractor .
```

------------------------------------------------------------------------

## \## 4. Run container

``` bash
docker run -p 8000:8000 --env-file .env pet-extractor
```

Server will start at:

    http://localhost:8000

------------------------------------------------------------------------

## \## 5. Test server

Open Swagger docs:

    http://localhost:8000/docs

Or test endpoint:

``` bash
curl http://localhost:8000/
```

------------------------------------------------------------------------

## \## 6. Stop container

Press:

    CTRL + C

Or stop manually:

``` bash
docker ps
docker stop <container_id>
```

------------------------------------------------------------------------

## \## 7. Optional: run in background

``` bash
docker run -d -p 8000:8000 --env-file .env pet-extractor
```

------------------------------------------------------------------------

You're all set 🚀
