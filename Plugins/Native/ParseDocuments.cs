using System.ComponentModel;
using Microsoft.SemanticKernel;


namespace Plugins.Native;

public class ParseDocuments
{
    [KernelFunction]
    [Description("Reads all files in the given folder and returns the content as a list of strings")]
    [return: Description("The raw file content of all files in a given folder")]
    public string GetFileContent(string filePath)
    {
        return string.Join(Environment.NewLine, Directory.GetFiles(filePath).Select(File.ReadAllText));
    }
}