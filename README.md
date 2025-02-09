# Interactive Query Engine with Streamlit

This project is an interactive query engine built using Streamlit and LlamaIndex. It allows users to query a set of documents and get answers based on the context provided by the documents.

## Project Structure

- `app.py`: The main Streamlit application file that sets up the user interface and initializes the query engine.
- `main.py`: Contains the main logic for setting up the query engine, including loading data, embedding documents, and creating the index.
- `original.py`: An alternative implementation of the query engine setup.
- `test-dir/`: Directory containing the input documents to be queried.
- `README.md`: This file.
- `.gitignore`: Specifies files and directories to be ignored by git.

## Setup and Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit application in your browser.
2. Enter your query in the input box.
3. The query engine will process your query and provide an answer based on the context of the documents in the [test-dir](http://_vscodecontentref_/5) directory.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.