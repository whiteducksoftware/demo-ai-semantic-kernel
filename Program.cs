using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;
using Plugins.Native;
using Spectre.Console;

AnsiConsole.Write(
    new FigletText("wd SAM Report Generator")
    .LeftJustified()
    .Color(Color.Orange3));

// Initialize Kernel
var settings = KernelSettings.LoadSettings();
var kernelbuilder = Kernel
    .CreateBuilder()
    .AddAzureOpenAIChatCompletion(settings.DeploymentOrModelId, settings.Endpoint, settings.ApiKey);

// Add plugins
kernelbuilder.Plugins.AddFromType<ParseDocuments>();
kernelbuilder.Plugins.AddFromPromptDirectory(Path.Combine("Plugins", "Semantic"));
var kernel = kernelbuilder.Build();

// Create a planner and execute the plan
var planner = new HandlebarsPlanner(new HandlebarsPlannerOptions() { AllowLoops = true });
var plan = await planner.CreatePlanAsync(kernel, "Read all content from the 'sample' folder. AFTER that, Create a list of findings using the file content as input");
var result = await plan.InvokeAsync(kernel);

// write the markdown output to a file
File.WriteAllText("output.md", result.ToString());
Console.WriteLine(result);
