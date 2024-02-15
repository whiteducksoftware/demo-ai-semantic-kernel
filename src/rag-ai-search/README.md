# Semantic Kernel demo project

This is a demo project for the Semantic Kernel. It is a .NET Core 8 console application that uses the Semantic Kernel to generate text using the OpenAI ChatGPT model.

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


