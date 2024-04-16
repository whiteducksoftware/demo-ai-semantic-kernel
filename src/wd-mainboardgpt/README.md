# MainboardGPT AI Project for RAG pattern demonstration

The goal of this project is to develop a proof of concept for a copilot that assists users with finding relevant information in a library of technical documentation. The project leverages the OpenAI GPT-3 model and integrates with the Azure OpenAI API.

## Prerequisites

All you need is an Azure OpenAI key. Simply adopt the following secrets to your values and execute them in the project folder:

```bash
dotnet user-secrets set "endpoint" "https://<OPENAINAME>.openai.azure.com/"
dotnet user-secrets set "deploymentOrModelId" "<MODELID>" #e. g. gpt-4-32k
dotnet user-secrets set "apiKey" "<APIKEY>"
dotnet user-secrets set "dataSourceEndpoint" "<AZUREAISEARCH.ENDPOINT>"
dotnet user-secrets set "dataSourceApiKey" "<AZUREAISEARCH.APIKEY>"
dotnet user-secrets set "dataSourceIndex" "<AZUREAISEARCH.INDEXNAME>"
```

After that, you can run the project using `dotnet run`.
