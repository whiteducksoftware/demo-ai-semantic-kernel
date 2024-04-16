using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Embeddings;

sealed class AzureAISearchPlugin
{
    private readonly ITextEmbeddingGenerationService _textEmbeddingGenerationService;
    private readonly IAzureAISearchService _searchService;

    public AzureAISearchPlugin(
        ITextEmbeddingGenerationService textEmbeddingGenerationService,
        IAzureAISearchService searchService)
    {
        this._textEmbeddingGenerationService = textEmbeddingGenerationService;
        this._searchService = searchService;
    }

    [KernelFunction("Search")]
    public async Task<string> SearchAsync(
        string query,
        string collection,
        List<string>? searchFields = null,
        CancellationToken cancellationToken = default)
    {
        // Convert string query to vector
        ReadOnlyMemory<float> embedding = await this._textEmbeddingGenerationService.GenerateEmbeddingAsync(query, cancellationToken: cancellationToken);

        var tmp = await this._searchService.SearchAsync(collection, embedding, searchFields, cancellationToken) ?? string.Empty;

        // Perform search
        return tmp;
    }
}