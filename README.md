## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/shouryade/LMTSM-Backend.git
   cd LMTSM-Backend
   ```
2. Make your you have Python 3.10 installed on your system. If not, you can download it from [here](https://www.python.org/downloads/).

3. Install pipenv by running the following command in your terminal:
   ```sh
   pip install pipenv
   ```
4. Install the dependencies
   ```sh
    pipenv install
   ```
5. Activate the virtual environment
   ```sh
   pipenv shell
   ```
6. Run the server
   ```sh
   pipenv run python -m app
   ```
7. The server should be up and running on http://localhost:8100

## Setting environment variables

1. Rename the `.env.sample` file to `.env`
2. Replace the values of the variables with your own values
3. Close the server by pressing `Ctrl + C` in the terminal.
4. Restart the server by running the following command:
   ```sh
   pipenv run python -m app
   ```

## Backend Documentation

You can access the documentation of the backend by visiting http://localhost:8100/docs
You can also try out the API endpoints by first authenticating and creating a user and setting their role to `super_admin` (using MongoDB Compass) and then using the `Try it out` button to make requests to the API.
