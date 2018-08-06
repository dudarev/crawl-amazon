Write a Python command line tool that scrapes data from Amazon.
The tool should be a “headless” crawler that does not open an external browser.

- Reads Amazon credentials from a file on the localhost.
- Reads a search string from the command line arguments.
- Logs into Amazon.
- Enters the search string into the Amazon search box and submits it.
- Print the product details of the first page of search results as text.
- Tool should run in Docker container
