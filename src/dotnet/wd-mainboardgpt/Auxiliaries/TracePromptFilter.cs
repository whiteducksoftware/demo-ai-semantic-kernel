using Microsoft.SemanticKernel;

/// <summary>
/// Prompt filter for observability.
/// </summary>
sealed class TracePromptFilter : IPromptFilter
{
    public TracePromptFilter()
    {

    }

    public void OnPromptRendered(PromptRenderedContext context)
    {
        Console.WriteLine($"Rendered prompt: {context.RenderedPrompt}");
    }

    public void OnPromptRendering(PromptRenderingContext context)
    {
        Console.WriteLine($"Rendering prompt for {context.Function.Name}");
    }
}
