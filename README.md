# Requirements
Direct command which can be run in Terminal to install all required dependencies:

`pip install pandas BeautifulSoup nltk syllapy`

Please provide a separate copy file of `Input` file and rename it as `Output` which can be used for the program to avoid formatting and memory issues. The provided file `Output Data Structure.xlsx` can also be used for the same but the program will create new columns for every text analysis factor which will later create issues in formatting.

# Definition of files
The codes have predefined format of Input, StopWords, MasterDictionary, Output Template, Output files and it is recommended to use absolute addresses if running locally.

### Addresses of predefined files and folders:
Change the following in the code itself as per requirements.

Input file: `Blackcoffer Test Assignment/Input.xlsx`

StopWords Folder: `Blackcoffer Test Assignment/StopWords`

MasterDictionary: `Blackcoffer Test Assignment/MasterDictionary`

Output Template: `Blackcoffer Test Assignment/Output.xlsx`

Output file: `Blackcoffer Test Assignment/Text Analysis Results.xlsx`

# Features
This program will access the URLs provided in `Input.xlsx` file, access the URLs and then extract the article content from the sites. After extraction, it'll export the articles in the form of their corresponding `URL_ID.txt` files inside a separate folder `articles`.

There are two different types of extraction process provided in the code: Single-threaded and Multi-threaded. Single threaded function is stable and applicable for all use but is slow in nature. Multithreaded function is significantly fast and configurable as per the number of allowed connections with the server. If the server does not allow multi connection to itself, single threaded function is recommended to use.

After extraction, the program begins text analysis as per the rules defined in `Text Analysis.docx`. The function will make use of `StopWords` and `MasterDictionary` provided with the assignment.

After extraction and text analysis, the program will export the obtained results in the format provided in `Output Data Structure.xlsx`. The program has been written to take the `Output.xlsx` as base structure and create new columns and fill them as per the order given in `Output Data Structure.xlsx` and save the file as `Text Analysis Results.xlsx`.

# Execution
The program can be executed using both Python file `Extract.py` or the Jupyter file `Extract.ipynb` in Google Colab or a system with Jupyter Notebooks compactibility.

For executing the Jupyter file, its is possible to directly run all cells in the notebook as long as the addresses of referenced files and folders (as given [above](#markdown-header-addresses-of-predefined-files-and-folders)). If running the file in Google Colab, the same files will be required to uploaded in the runtime and referenced correctly.

For executing the Python file, simply run it by using `python Extract.py`. Keep note of the addresses and references used in the code.

# Known Issues
Following is(are) the known issue(s) which impact the accuracy of the program:
- When extracting content that are in the form of lists, they are extracted twice. 
