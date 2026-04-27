using System.IO.Compression;

namespace MaiConverter.Custom.Core.Services;

public static class ZipService
{
    public static void ZipDirectory(DirectoryInfo sourceDir, FileInfo zipFile, bool overwrite = true)
    {
        if (!sourceDir.Exists)
        {
            throw new DirectoryNotFoundException(sourceDir.FullName);
        }

        if (zipFile.Exists)
        {
            if (!overwrite)
            {
                return;
            }

            zipFile.Delete();
        }

        ZipFile.CreateFromDirectory(sourceDir.FullName, zipFile.FullName);
    }

    public static void ZipFolderAndMaybeDelete(DirectoryInfo sourceDir, bool deleteAfter, bool overwrite = true, string extension = ".zip")
    {
        var outPath = new FileInfo(Path.ChangeExtension(sourceDir.FullName, extension));
        ZipDirectory(sourceDir, outPath, overwrite);
        if (deleteAfter)
        {
            sourceDir.Delete(true);
        }
    }

    public static IReadOnlyList<FileInfo> ZipImmediateSubfolders(DirectoryInfo outputRoot, bool deleteAfter, bool overwrite = true, string extension = ".zip")
    {
        if (!outputRoot.Exists)
        {
            return Array.Empty<FileInfo>();
        }

        var zips = new List<FileInfo>();
        foreach (var dir in outputRoot.EnumerateDirectories())
        {
            var outPath = new FileInfo(Path.ChangeExtension(dir.FullName, extension));
            ZipDirectory(dir, outPath, overwrite);
            zips.Add(outPath);
            if (deleteAfter)
            {
                dir.Delete(true);
            }
        }

        return zips;
    }
}
