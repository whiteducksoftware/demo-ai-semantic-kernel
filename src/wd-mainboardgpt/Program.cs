using Azure;
using Azure.Search.Documents.Indexes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.SemanticKernel;

using Spectre.Console;

AnsiConsole.Write(
    new FigletText("white duck mainboardGPT")
    .LeftJustified()
    .Color(Color.Orange3));

var model = AnsiConsole.Prompt(
    new SelectionPrompt<string>()
        .Title("Please select your mainbord model:")
        .HighlightStyle(new Style().Foreground(Color.Orange1))
        .AddChoices([
            "asrock-fatal1ty-z87-killer",
            "asrock-p5b-de",
            "asus-g22451-prime-h610m-d",
            "gigabyte-b650-eagle-ax"]));


KernelArguments variables = new()
{
    ["model"] = model
};

// Initialize Kernel
var settings = KernelSettings.LoadSettings();
var kernelbuilder = Kernel
    .CreateBuilder()
    .AddAzureOpenAIChatCompletion(settings.DeploymentOrModelId, settings.Endpoint, settings.ApiKey);

Uri endpoint = new(settings.DataSourceEndpoint);
AzureKeyCredential keyCredential = new(settings.DataSourceApiKey);

kernelbuilder.Services.AddSingleton((_) => new SearchIndexClient(endpoint, keyCredential));
kernelbuilder.Services.AddSingleton<IAzureAISearchService, AzureAISearchService>();
kernelbuilder.AddAzureOpenAITextEmbeddingGeneration("ada", settings.Endpoint, settings.ApiKey);
kernelbuilder.Plugins.AddFromType<AzureAISearchPlugin>();

var kernel = kernelbuilder.Build();
var prompts = kernel.ImportPluginFromPromptDirectory(@"./Plugins/Prompts");

var resultsByPrompt = new Dictionary<KernelFunction, Task<FunctionResult>>();

await AnsiConsole.Status()
    .AutoRefresh(true)
    .Spinner(Spinner.Known.Default)
    .SpinnerStyle(Style.Parse("orange1"))
    .StartAsync("[orange1]Thinking...[/]", async ctx =>
    {
        foreach (var p in prompts)
        {
            resultsByPrompt[p] = kernel.InvokeAsync(p, variables);
        }

        await Task.WhenAll(resultsByPrompt.Values);
    });

// Create a table
var table = new Table();

// Add some columns
foreach (var kvp in resultsByPrompt)
{
    table.AddColumn(kvp.Key.Name);
}

table.AddRow(resultsByPrompt.Values.Select(t => t.Result.ToString()).ToArray());

// Render the table to the console
AnsiConsole.Write(table);

DumpOutput.Dump($"./output/{model}.md",
    resultsByPrompt.Select(kvp => Tuple.Create(kvp.Key.Name, kvp.Value.Result.ToString())).ToList());

