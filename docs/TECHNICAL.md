# Technical documentation

## How it works

The Windows Forms frontend launches the adjacent `IndexedSearch.py` backend through the Python launcher (`py -3`), or through `python.exe` beside the app if present. Python's SQLite FTS5 trigram index stores full decoded lines and enables substring searches. The database and status files are in `%LOCALAPPDATA%\UltraMegaTextSearchTool`. The UI asks for a source folder on the first build and remembers it there. The source and database paths are passed to the backend through environment variables.

The backend recursively enumerates source files. Each file is indexed in a separate transaction with 10,000-line batches, then recorded in the `completed` table with its path, size, modification time and row count. Resume skips unchanged completed files; errors or a pause roll back the current file. A changed indexed file requires a fresh database. Size and timestamp are not cryptographic integrity checks; keep source files unchanged.

Progress is completed source bytes divided by total source bytes, excluding the current file until committed. The UI and backend use a JSON status file and stop flag. A Windows mutex prevents concurrent builds started through the app. SQLite uses WAL mode, NORMAL synchronous mode and a 256 MiB cache target. Database, WAL and temporary files can greatly exceed source size. The builder attempts to pause below 20 GiB free, but an active transaction may consume space between checks. CPU, storage, cache and content all affect speed.

Queries use a quoted FTS expression followed by a literal substring check. Queries must have at least three characters. The result filter operates on the returned in-memory lines, ignoring case; it does not query the database again. The result limit applies before filtering. Files are decoded as UTF-8 with replacement for invalid bytes. FTS Unicode case folding and the literal check may differ in edge cases. There is no encryption, provenance per result or automatic reindexing.

## Requirements and source build

Windows with .NET Framework 4.x and Python 3 with SQLite FTS5 trigram support are required. The packaged executable expects `IndexedSearch.py` beside it. Build the frontend from the repository root with the .NET Framework C# compiler:

```bat
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:winexe /out:"Ultra Mega Text Search Tool.exe" /win32icon:"assets\Ultra Mega icon.ico" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.Web.Extensions.dll src\BreachSearch.cs
```

The root `IndexedSearch.py` is the runtime copy of `src/IndexedSearch.py`; update both when changing the backend. Do not commit source collections, databases, WAL files, status files, results or credentials. Search data stays local during ordinary operation. The developer credit opens a browser only when clicked.
