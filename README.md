# REST-API LLM RAG

This application provides an API service that retrieves answers to user queries based on the given context.

- **Context Management**: Context is managed and stored using [FAISS](https://github.com/facebookresearch/faiss).
- **Chat Service Interfaces**: The application supports two interfaces: **Hugging Face** and **OpenAI**, both requiring an API key for access.
- **Supported Document Formats**: The app can process documents in various formats, such as PDF and TXT.
- **Core Libraries**: This project uses FastAPI and LangChain as its core libraries.
- **Docker Ready**: The project is configured for containerization with Docker.

> 💡 For structured data types like CSV, XLSX, SQL, etc., it's recommended to utilize LLM Agents.

> 💡 The Docker image is built using a CUDA-enabled Docker base image ([`nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04`](https://hub.docker.com/layers/nvidia/cuda/12.6.3-cudnn-runtime-ubuntu24.04/images/sha256-23debbe74125dc84df96df79cff42079b3b15265c27140714fd27b5aa718faa4)), which allows GPU acceleration during execution.

> 💡 If you want to use a Hugging Face models, make sure to choose a larger model, such as one with 70B parameters, to achieve better results.

## 🛠️ Configuration

To set up the application, follow these steps:

1. Clone the repository and navigate to the project directory:
```bash
git clone git@github.com:asp1420/restapi-rag.git
cd restapi-rag
```

2. Set the API key environment variable in the `rag/.env` file:

- **Hugging Face**: Set the API key in the `HF_TOKEN` environment variable.
- **OpenAI**: Set the API key in the `OPENAI_API_KEY` environment variable.

If both API keys are configured, the OpenAI service will be used by default.

3. Set the LLM chat and embedding model environment variables:  

- **Embedding Model**: Set the embedding model in the `EMBEDDING_MODEL` environment variable. Default `nomic-ai/nomic-embed-text-v1.5`.
- **LLM Chat Model**: Set the LLM chat model in the `LLM_MODEL` environment variable. Default `meta-llama/Llama-3.2-1B-Instruct`

If you choose the Hugging Face LLM chat model, set the `HF_HOME` variable to `models`, meaning the models will be stored in the `rag/models` directory. This setup ensures that models used by the app are separated and ready for Docker containerization.

## ⚙️ Installation and execution

### 📦 Docker

Follow these steps to build the Docker image and run the container:

1. Build the Docker image. 

> ⚠️ Important: Before building the Docker image, make sure to run the app once to download the embeddings and/or LLM chat models in the directory specified by `HF_HOME`.

```bash
docker build -t [image name] rag/
```

2. Run the container.

```bash
docker run --rm --env-file rag/.env --gpus all --volume [local volume path]:/api/db --name [container name] [image name]
```

### 💻 Locally

To run the app locally, follow these steps:

1. Install the required libraries from the requirements.txt file.
2. Set the environment variables as defined in the Configuration section.
3. Start the app with the following command:

```bash
python -m uvicorn app.main:app
```

4. Navigate to `http://127.0.0.1:8000/docs` to access the app's documentation.

## 🗂️ Documentation

You can access the API documentation once the application is running. To do so, follow these steps:

1. Run the container.
2. Retrieve the container's IP address:

```bash
docker inspect [container name] | grep IPAddress
```

3. Access the documentation via your web browser.

> 💡 General documentation: `http://[IP]:8080/docs` and endpoint documentation: `http://[IP]:8080/redoc`.


## 📝 TODO

- [ ] Create an endpoint that lists FAISS collections/topics.
- [ ] Implement an endpoint to update the collections.
- [ ] Implement an endpoint to delete a selected collection.
