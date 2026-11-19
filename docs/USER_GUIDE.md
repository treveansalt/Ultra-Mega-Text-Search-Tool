# Basic user guide

## Set up

1. Install Python 3 for Windows from [python.org](https://www.python.org/downloads/windows/). Include the Python launcher when installing. Python's SQLite must support the FTS5 trigram tokenizer.
2. Download and extract all the project files into a folder on your computer. Keep `Ultra Mega Text Search Tool.exe` and `IndexedSearch.py` together.
3. Open **Ultra Mega Text Search Tool.exe**.

## Build the database

Click **Start build** and choose **Yes** for a single text file, or **No** for a folder containing text files. For a folder, files inside subfolders are indexed too. The app remembers your selection. The database is stored under the current user's local app-data folder, in `UltraMegaTextSearchTool`. Allow plenty of free disk space; the index can be larger than the original files.

Wait until the app says **Build complete**. You can click **Pause build** and later **Resume build**; completed files are retained, while the current file may need to be retried. The percentage shows the size of completed files, so it may stay unchanged while a large file is processed. Searches during a build cover only files already indexed.

Keep the source files unchanged during indexing. If an already indexed file changes, a fresh database is required. To build a different collection, close the app and move or remove the `UltraMegaTextSearchTool` folder from your Windows local app-data folder, then reopen the app and choose a new source file or folder. This removes the existing index, so keep a backup if you need it.

## Search

Enter at least three characters and click **Search**. Enable **Case sensitive** before searching if needed. To narrow the returned lines further, type in **Filter returned results**; clear it to show all returned lines. The filter searches only the results already returned. Click **Stop search** to cancel a search. Click **Export results** and choose a filename and location to save the currently displayed (filtered) results as a UTF-8 text file. An unfiltered export includes all returned results. Very broad searches can use substantial memory and take time.

The database and displayed lines can contain sensitive information. Search only files you are authorized to use. A missing result does not prove text has never appeared in another collection.

## Jokes

Click **Jokes** for a retro falling-letters animation inspired by Cascade. Click **Stop Jokes** to return to the normal display. The effect is confined to the app window and does not change files or search results.

## Troubleshooting

- If Python cannot be found, install Python 3 for Windows with the Python launcher and reopen the app.
- If indexing pauses for low disk space, free space on the drive containing your local app-data folder and resume. The app pauses when less than 20 GiB remains.
- If the database reports an FTS5 or trigram error, install a Python distribution whose SQLite includes FTS5 and trigram support.
