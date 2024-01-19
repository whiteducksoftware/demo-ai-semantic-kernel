// using Microsoft.SemanticKernel;

// internal static class KernelBuilderExtensions
// {
//     /// <summary>
//     /// Adds a Azure chat completion service to the list.
//     /// </summary>
//     /// <param name="kernelBuilder"></param>
//     /// <param name="kernelSettings"></param>
//     /// <exception cref="ArgumentException"></exception>
//     internal static KernelBuilder WithCompletionService(this KernelBuilder kernelBuilder, KernelSettings kernelSettings)
//     {

//         return kernelBuilder.WithAzureChatCompletionService(
//             deploymentName: kernelSettings.DeploymentOrModelId, endpoint: kernelSettings.Endpoint, apiKey: kernelSettings.ApiKey);
//     }
// }
