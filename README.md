# blazor-qr-code-generator

This is a .Net core blazor application for generating QR code. The application can be containerize and it contains an end to end test using selenium in python

## Technology Stack & Tools

- .Net core C# (language used in the project)
- Blazor (Web technology)
- Selenium (Testing framework)
- Python (language used in the test)
- [Docker](https://www.docker.com/) (Containerizing applications)

## Start Development

- Kindly fork and clone the repo 

- cd to the app folder from the root folder in your terminal and enter the following command

To run only the application
```
dotnet run 
```

To run e2e test

```
pytest e2etest/evals.py
```

To run both application and e2e test

```
sh run.sh
```

To create an image from this project, you will need to have docker installed and enter the following command

```
Docker build -t qr_code .
```

To run the docker image, enter the following command

```
Docker run -it -p 5000:5000 qr_code
```

## :brain: Author

- IJONI VICTOR 😁😁😁

> Please :pray: don't forget to star :star: the project 😁😁 . Thanks :+1: