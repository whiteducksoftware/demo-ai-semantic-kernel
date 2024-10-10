using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Spectre.Console;

AnsiConsole.Write(
    new FigletText("wd RAG Chatbot")
    .LeftJustified()
    .Color(Color.Orange3));

// Initialize Kernel
var settings = KernelSettings.LoadSettings();

var config = new AzureOpenAIChatCompletionWithDataConfig
{
    CompletionModelId = settings.DeploymentOrModelId,
    CompletionEndpoint = settings.Endpoint,
    CompletionApiKey = settings.ApiKey,
    DataSourceEndpoint = settings.DataSourceEndpoint,
    DataSourceApiKey = settings.DataSourceApiKey,
    DataSourceIndex = settings.DataSourceIndex
};

var kernelbuilder = Kernel
    .CreateBuilder()
    .AddAzureOpenAIChatCompletion(config);

var kernel = kernelbuilder.Build();

var function = kernel.CreateFunctionFromPrompt("Question: {{$input}}");

while (true)
{
    AnsiConsole.Write(new Rule());
    var prompt = AnsiConsole.Ask<string>("[bold]What is your question?[/]");
    var response = await kernel.InvokeAsync(function, new() { ["input"] = prompt });
    AnsiConsole.WriteLine(response.ToString());
}
