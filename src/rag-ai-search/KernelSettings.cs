using System.Text.Json.Serialization;
using Microsoft.Extensions.Configuration;

internal class KernelSettings
{
    [JsonPropertyName("deploymentOrModelId")]
    public string DeploymentOrModelId { get; set; } = string.Empty;

    [JsonPropertyName("endpoint")]
    public string Endpoint { get; set; } = string.Empty;

    [JsonPropertyName("apiKey")]
    public string ApiKey { get; set; } = string.Empty;

    [JsonPropertyName("dataSourceEndpoint")]
    public string DataSourceEndpoint { get; set; } = string.Empty;

    [JsonPropertyName("dataSourceApiKey")]
    public string DataSourceApiKey { get; set; } = string.Empty;

    [JsonPropertyName("dataSourceIndex")]
    public string DataSourceIndex { get; set; } = string.Empty;


    /// <summary>
    /// Load the kernel settings from settings.json if the file exists and if not attempt to use user secrets.
    /// </summary>
    internal static KernelSettings LoadSettings()
    {
        try
        {
            
            return FromUserSecrets();
        }
        catch (InvalidDataException ide)
        {
            Console.Error.WriteLine(
                "Unable to load semantic kernel settings, please provide configuration settings using instructions in the README.\n" +
                "Please refer to: https://github.com/microsoft/semantic-kernel-starters/blob/main/sk-csharp-hello-world/README.md#configuring-the-starter"
            );
            throw new InvalidOperationException(ide.Message);
        }
    }

    /// <summary>
    /// Load the kernel settings from user secrets.
    /// </summary>
    internal static KernelSettings FromUserSecrets()
    {
        var configuration = new ConfigurationBuilder()
            .AddUserSecrets<KernelSettings>()
            .Build();

        return configuration.Get<KernelSettings>()
               ?? throw new InvalidDataException("Invalid semantic kernel settings in user secrets, please provide configuration settings using instructions in the README.");
    }
}
