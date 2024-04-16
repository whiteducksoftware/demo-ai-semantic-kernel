public static class DumpOutput
{
    public static void Dump(string fileName, List<Tuple<string, string>> args)
    {
        File.WriteAllText(fileName, string.Join(Environment.NewLine, args.Select(x => $"# {x.Item1} {Environment.NewLine} {x.Item2}")));
    }
}