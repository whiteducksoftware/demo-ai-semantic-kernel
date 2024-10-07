/// <summary>
/// Abstraction for Azure AI Search service.
/// </summary>
interface IAzureAISearchService
{
    Task<string?> SearchAsync(
        string collectionName,
        ReadOnlyMemory<float> vector,
        List<string>? searchFields = null,
        CancellationToken cancellationToken = default);
}