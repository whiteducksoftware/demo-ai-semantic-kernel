using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;
using Plugins.Native;
using Spectre.Console;



AnsiConsole.Write(
    new FigletText("wd SAM Report Generator")
    .LeftJustified()
    .Color(Color.Orange3));

var kernelSettings = KernelSettings.LoadSettings();

var kernelbuilder = Kernel.CreateBuilder().AddAzureOpenAIChatCompletion(modelId: kernelSettings.DeploymentOrModelId, apiKey: kernelSettings.ApiKey, deploymentName: kernelSettings.DeploymentOrModelId, endpoint: kernelSettings.Endpoint);

kernelbuilder.Plugins.AddFromType<ParseDocuments>();
var kernel = kernelbuilder.Build();

var skillsDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Plugins");
kernel.ImportPluginFromPromptDirectory(skillsDirectory, "Semantic");

var planner = new HandlebarsPlanner(new HandlebarsPlannerOptions() { AllowLoops = true });

var plan = await planner.CreatePlanAsync(kernel, "Read all content from ./sample folder. AFTER that, Create a list of findings using the FILE_CONTENT as the $input parameter");


var result = await plan.InvokeAsync(kernel);
// write the markdown output to a file
File.WriteAllText("output.md", result.ToString());

// result contains markdown. Write it using Spectre.Console
Console.WriteLine(result);
