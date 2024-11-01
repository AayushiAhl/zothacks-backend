# hacknights-w-2024-template-flask
Enter a URL to call an API and see its response!

Sample API (Enter this into the box at the top once you successfully run the app!): https://swapi.dev/api/planets/1/

## 1. Pre-requisites

Ensure that you have Python installed. If you do not, see [here](https://www.python.org/downloads/) to download it.

## 2. Project Setup

1. Clone this repository

    Using HTTPS:
    ```shell
    git clone https://github.com/IanWearsHat/hacknights-w-2024-template-flask.git
    ```

    or SSH (you would need to set up an SSH key. See [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) for more information, otherwise use HTTPS):
    ```shell
    git clone git@github.com:IanWearsHat/hacknights-w-2024-template-flask.git
    ```

2. Create a virtual environment

    This isolates the libraries you install in this environment from the libraries on your actual machine, preventing conflicts between libraries.

    ```shell
    python3 -m venv .venv
    ```

3. Activate virtual environment

   VS Code may prompt to automatically select the newly created virtual environment.
   Otherwise, for Mac/Linux, run

   ```shell
   source .venv/bin/activate
   ```
   and for Windows, run

   ```shell
   .\.venv\scripts\activate
   ```

4. Install dependencies
   ```shell
   pip install -r requirements.txt
   ```

   This will install all of the packages that you need for the python files to work.

## 3. Running the app

Run this command:
```shell
flask run
```

and a server will run at http://127.0.0.1:5000 (or http://localhost:5000).

*Note*: changing any Python code will not update the server that is running. You must stop the server and re-run ```flask run``` to see any changes.

However, if you run
```shell
flask run --debug
```
Flask will automatically reload itself if you change the Python code. This also enables an interactive debugger.
