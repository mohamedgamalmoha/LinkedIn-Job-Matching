# Job Matching API

The Job Matching API is a Flask-based web application that allows users to match their skills and education criteria with job requirements. It provides an endpoint to perform the job matching and returns a matching score indicating the compatibility between the user and the job.


## Features

- User authentication using JWT
- Scrapping LinkedIn to fetch job listings
- Matching algorithm based on employee criteria and job requirements
- Testing with Flask-Testing


## Installation

1. Clone the repository:
   ```shell
   git clone https://github.com/your-username/job-matching-api.git
   ```
   
2. Install virtual environment package - outside project directory -, then activate it:
    ```shell
    pip install virtualenv
    virtualenv env
    ```

3. Activate the virtual environment:
   - For Unix/macOS:
     ```shell
     source venv/bin/activate
     ```
     
   - For Windows:
     ```shell
     venv\Scripts\activate
     ```
     
4. Navigate to the project directory:
   ```shell
   cd job-matching-api
   ```
   
5. Install the dependencies:
   ```shell
   pip install -r requirements.txt
   ```

6. Set up the environment variables: \
   Create a `.env` file in the root (**`web`**) directory of the project and add the following variables:
    ```.dotenv
    SECRET_KEY=your-secret-key
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=sqlite:///site.db
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    WTF_CSRF_ENABLED=False
    JWT_SECRET_KEY=your-jwt-secret-key
    ```

8. Start the application:

   ```shell
   python run.py
   ```

9. The application will be accessible at `http://localhost:5000`.


## Usage

- Register a new user using the `/api/auth/signup` endpoint.
    ```shell
    curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "email": "your_email@example.com", "password": "your_password", "confirm_password": "your_confirm_password"}' http://localhost:5000/api/auth/signup
    ```
- Log in with the registered user using the `/api/auth/login` endpoint to obtain a JWT token.
    ```shell
    curl -X POST -H "Content-Type: application/json" -d '{"email":"john@gmail.com", "password":"password123"}' http://localhost:5000/api/auth/login
    ```
- Delete user by using the `/api/auth/delete` endpoint.
    ```shell
    curl -X DELETE -H "Authorization: Bearer <JWT>" "http://localhost:5000/api/auth/delete?user_id=<USER_ID>"
    ```
- Use the obtained JWT token in the `Authorization` header for protected endpoints.
- Perform job matching using the `/api/job-matching` endpoint by providing employee criteria and job data.
    ```shell
    curl -X GET -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"location": "your_location","keywords": "kw1,kw2","education": "your_education","skills": "sk1,sk2","start": 1}' "http://localhost:5000/api/job-matching"
    ```
    The server will return a JSON object called `job_listings` contains list of matched jobs as following:
    ```json
    {
      "title":"job title",
      "company":"company name",
      "description":"job description",
      "score": "matching score"
    }
   ```
   here is the explanation of each field of results:
   - **title:** The title of that job. 
   - **company:** The name of the company that offers that job. 
   - **description:** The detailed description of that job. 
   - **score:** The matching score between user skills and detailed description.


## Testing

To run the tests, use the following command - before you run the test, make sure you have a good internet connection - :

```shell
python -m unittest test.py
```


## Notes

- The entire project relies on web scraping, which means that the frontend of LinkedIn may undergo modifications in the future. If such changes occur, make sure to modify the `parser.py` file accordingly in order to adapt to the new structure.
- To prevent the sender's IP from being blocked due to multiple requests being sent to LinkedIn, it is advisable to rely on a proxy server provider, especially when working in a production environment. This approach ensures a safer and more secure operation.


## Built With
This application was built with the help of ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture. ChatGPT provided natural language processing capabilities that were used to implement the image-to-text extraction feature.
For more information on ChatGPT and its capabilities, check out the [ChatGPT documentation](https://beta.openai.com/docs/guides/chat-gpt). To learn more about OpenAI and its mission to ensure that artificial intelligence benefits humanity, visit the [OpenAI website](https://openai.com/).


## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you would like to contribute code changes or suggest new features.


## License
This project is licensed under [MIT License](https://opensource.org/licenses/MIT).