# PDF Question Answering App

This application allows users to perform question answering on PDF files. Users can upload a PDF file, input their OpenAI API key, ask questions related to the content of the PDF, and receive answers displayed in the browser.

## Features

- Upload a PDF file.
- Input OpenAI API key for question answering.
- Ask questions related to the content of the PDF.
- Display answers in the browser.
- Advanced settings for question answering.

## Prerequisites

- Docker installed on your machine.

## Usage

1. Clone this repository:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project-directory>
    ```

3. Build the Docker image:

    ```bash
    docker build -t pdf-qa-app .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 8888:8888 pdf-qa-app
    ```

5. Open your web browser and go to `http://localhost:8888`.

6. Follow the on-screen instructions to use the application.

## Configuration

- Change the port mapping (`-p`) in the `docker run` command to run the application on a different port if needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
