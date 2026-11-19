# Ultra Mega Text Search Tool

A Windows application for searching large collections of text files locally. Build a database once, then find text quickly and filter the results. Developed by [treveansalt](https://github.com/treveansalt/) with added AI Slop.

![Retro search logo](assets/Ultra%20Mega%20logo.png)

## Get started

1. Install [Python 3 for Windows](https://www.python.org/downloads/windows/), including the Python launcher. A version with SQLite FTS5 trigram support is required.
2. Download the repository as a ZIP and extract all files to a folder on your computer.
3. Run **Ultra Mega Text Search Tool.exe**. Keep `IndexedSearch.py` in the same folder as the app.
4. Click **Start build**, choose the folder containing your text files, and wait for the database to finish.
5. Enter at least three characters and click **Search**. Use **Filter returned results** to narrow the results already found.

The database is stored in the current Windows user's local app-data folder. Indexing can take a long time and needs substantial free disk space. Searches are incomplete until the build finishes. The app runs locally; the database and results may contain sensitive plaintext.

Read the [basic user guide](docs/USER_GUIDE.md) or [technical documentation](docs/TECHNICAL.md) for details. The repository contains no text collections or databases. No licence has been specified; all rights are reserved by default.
