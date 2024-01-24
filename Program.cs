using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planners;
using Spectre.Console;

AnsiConsole.Write(
    new FigletText("wd SAM Report Generator")
    .LeftJustified()
    .Color(Color.Orange3));

var kernelSettings = KernelSettings.LoadSettings();
var kernel = new KernelBuilder()
    .WithCompletionService(kernelSettings)
    .Build();

var skillsDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Plugins");
kernel.ImportSemanticFunctionsFromDirectory(skillsDirectory, "Semantic");

// import native functions
kernel.ImportFunctions(new Plugins.Native.ParseDocuments(), "ParseDocuments");
var planner = new SequentialPlanner(kernel);
var plan = await planner.CreatePlanAsync("Read all content from ./sample folder. AFTER that, Create a list of findings using the file content as input");

var result = await plan.InvokeAsync(kernel);
// write the markdown output to a file
File.WriteAllText("output.md", result.ToString());

// result contains markdown. Write it using Spectre.Console
Console.WriteLine(result);
