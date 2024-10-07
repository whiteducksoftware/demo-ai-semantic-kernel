using System.Text;
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Models;

/// <summary>
/// Implementation of Azure AI Search service.
/// </summary>
sealed class AzureAISearchService : IAzureAISearchService
{
    private readonly List<string> _defaultVectorFields = new() { "contentVector" };

    private readonly SearchIndexClient _indexClient;

    public AzureAISearchService(SearchIndexClient indexClient)
    {
        this._indexClient = indexClient;
    }

    public async Task<string?> SearchAsync(
        string collectionName,
        ReadOnlyMemory<float> vector,
        List<string>? searchFields = null,
        CancellationToken cancellationToken = default)
    {
        // Get client for search operations
        SearchClient searchClient = this._indexClient.GetSearchClient(collectionName);

        // Use search fields passed from Plugin or default fields configured in this class.
        List<string> fields = searchFields is { Count: > 0 } ? searchFields : this._defaultVectorFields;

        // Configure request parameters
        VectorizedQuery vectorQuery = new(vector);
        fields.ForEach(field => vectorQuery.Fields.Add(field));

        SearchOptions searchOptions = new() { VectorSearch = new() { Queries = { vectorQuery } } };

        // Perform search request
        Response<SearchResults<IndexSchema>> response = await searchClient.SearchAsync<IndexSchema>(searchOptions, cancellationToken);
        // Console.WriteLine(response.GetRawResponse().Content);

        List<IndexSchema> results = new();

        // Collect search results
        await foreach (SearchResult<IndexSchema> result in response.Value.GetResultsAsync())
        {
            results.Add(result.Document);
        }

        // Return text from first result.
        // In real applications, the logic can check document score, sort and return top N results
        // or aggregate all results in one text.
        // The logic and decision which text data to return should be based on business scenario. 

        var sB = new StringBuilder();
        foreach (var result in results)
        {
            if (sB.Length > 0 && sB.Length >= 5000)
            {
                break;
            }

            sB.Append(result.Chunk);
        }

        return sB.ToString();
    }
}