# code-snippet-generator

## Getting Started

### Create ENV File
Create an .env file to add Postgres DB configs and OpenAI API Key. The file should look like this:

OPEN_AI_API=<Insert OpenAI Key>
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="postgres"
DB_PASSWORD="password"
DB_DATABASE="code_snippet"

### Installing Ollama Library and Running Llama2 Locally
Run the command below to download and install Ollama
```
curl -fsSL https://ollama.com/install.sh | sh
```

Once the instllation is complete the ru the Llama2 model using the command below:
```
ollama run llama2
```

After that you could access the llama2 using the API Endpoint. To test if the model is deploy you can use the following:
```
curl http://localhost:11434/api/chat -d '{
  "model": "mistral",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'
```

## Docker Commands

### Docker Command to run postgres container to connect database.
```
sudo docker build -t my-postgres-image -f Dockerfile_postgres .
```

```
sudo docker run -d --name my-postgres-container --restart always -p 5432:5432 -v postgres:/var/lib/postgresql/data my-postgres-image
```

### Docker Command to run code-snippet container.
```
sudo docker build -t code-snippet -f Dockerfile_code .
```

```
sudo docker run -d -p 5001:5001 code-snippet
```

## To Run this application

1. First install the required requirements using pip install -r requirements.txt
2. After installing requirements type
   python main.py
3. visit
   http://localhost:5001/
4. Application will start running, to use GPT Model, select GPT, to use custom model select Custom LLM
