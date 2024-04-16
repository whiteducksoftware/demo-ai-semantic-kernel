using System.Text.Json.Serialization;

sealed class IndexSchema
{
    [JsonPropertyName("chunk_id")]
    public string? ChunkId { get; set; }

    [JsonPropertyName("parent_id")]
    public string? ParentId { get; set; }

    [JsonPropertyName("content")]
    public string? Chunk { get; set; }

    [JsonPropertyName("title")]
    public string? Title { get; set; }

    [JsonPropertyName("contentVector")]
    public ReadOnlyMemory<float> Vector { get; set; }
}