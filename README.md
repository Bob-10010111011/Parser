
Course Scraper & Database Builder
A small ETL‑style Python project that downloads course data from online.dr-chuck.com, parses it, stores it in SQLite, and manages output files with conflict‑safe renaming and directory handling.

Features
-Downloads HTML from the source website
-Parses course names and links
-Stores data in SQLite with unique constraints
-Automatically creates tables if missing
-Generates DB file with user‑defined name + current date
-Moves output files into user‑selected or default directory
-Renames files if duplicates exist
-Cleans up cache directories
-Full logging of all operations



Project Structure

 Main.py
 Parser.py
 Database.py
 Save_to.py
 Move.py



How It Works
1.Check if sourse.html exists; otherwise download it
2.Parse headers and links
3.Create or update SQLite database
4.Ask user where to save output files
5.Move files into the chosen directory
6.Clean cache and temporary files
7.Log all steps



Usage
Run:
-python Main.py

Follow the prompts:
-Enter database name
-Choose default or custom directory
-Provide path if needed



Requirements
-Python 3.10+
-beautifulsoup4



Install dependencies:
-pip install beautifulsoup4

License
MIT License.

