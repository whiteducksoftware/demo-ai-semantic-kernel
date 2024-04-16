using Azure;
using Azure.Search.Documents.Indexes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;
using Spectre.Console;

AnsiConsole.Write(
    new FigletText("white duck mainboardGPT")
    .LeftJustified()
    .Color(Color.Orange3));

var mode = AnsiConsole.Prompt(
    new SelectionPrompt<string>()
        .Title("Please select the mode:")
        .HighlightStyle(new Style().Foreground(Color.Orange1))
        .AddChoices(new[] { "Discrete Prompts", "Planner" }));

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

switch (mode)
{
    case "Discrete Prompts":
        await UseDiscretePrompts();
        break;
    case "Planner":
        await UsePlanner();
        break;
}

async Task UseDiscretePrompts()
{
    var resultsByPrompt = new Dictionary<KernelFunction, FunctionResult>();

    await AnsiConsole.Status()
        .AutoRefresh(true)
        .Spinner(Spinner.Known.Default)
        .SpinnerStyle(Style.Parse("orange1"))
        .StartAsync($"[orange1]Executing {prompts!.Count()} prompts ... [/]", async ctx =>
        {
            foreach (var p in prompts)
            {
                AnsiConsole.MarkupLine($"[grey]LOG:[/] Retrieving {p.Name}[grey]...[/]");
                resultsByPrompt[p] = await kernel!.InvokeAsync(p, variables);
            }
        });

    // Create a table
    var table = new Table();

    // Add some columns
    foreach (var kvp in resultsByPrompt)
    {
        table.AddColumn(kvp.Key.Name);
    }

    table.AddRow(resultsByPrompt.Values.Select(t => t.ToString()).ToArray());

    // Render the table to the console
    AnsiConsole.Write(table);

    DumpOutput.Dump($"./output/{model}.md",
        resultsByPrompt.Select(kvp => Tuple.Create(kvp.Key.Name, kvp.Value.ToString())).ToList());
}

async Task UsePlanner()
{
    var planner = new HandlebarsPlanner(new HandlebarsPlannerOptions() { AllowLoops = true });

    HandlebarsPlan? plan = null;

    await AnsiConsole.Status()
        .AutoRefresh(true)
        .Spinner(Spinner.Known.Default)
        .SpinnerStyle(Style.Parse("orange1"))
        .StartAsync("[orange1]Generating plan ... [/]", async ctx =>
        {
            plan = await planner.CreatePlanAsync(kernel, $"Retrieve information about the ${{{model}}} motherboard's memory support and CPU Socket. Answer in the following format: Memory: [Supported Memory], CPU Socket: [CPU Socket].");
        });

    var table = new Table();
    table.AddColumn("Generated Plan:");
    table.AddRow(plan?.ToString() ?? "No plan generated");
    AnsiConsole.Write(table);

    string? result = null;

    await AnsiConsole.Status()
        .AutoRefresh(true)
        .Spinner(Spinner.Known.Default)
        .SpinnerStyle(Style.Parse("orange1"))
        .StartAsync("[orange1]Executing plan ... [/]", async ctx =>
        {
            if (plan != null)
            {
                result = await plan.InvokeAsync(kernel);
            }
        });

    table = new Table();
    table.AddColumn("Plan execution result:");
    table.AddRow(Markup.Escape(result!));
    AnsiConsole.Write(table);
}
