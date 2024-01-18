using System.ComponentModel;
using Microsoft.SemanticKernel;


namespace Plugins.Native;

public class ParseDocuments
{
    [SKFunction, Description("Reads all files in the given folder and returns the content as a list of strings")]
    public string GetFileContent(string filePath)
    {
        return string.Join(Environment.NewLine, Directory.GetFiles(filePath).Select(File.ReadAllText));
    }
}