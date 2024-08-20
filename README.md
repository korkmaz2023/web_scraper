# Generalized Web Scraping App

This repository contains a Streamlit-based web application that allows users to scrape data from websites by checking the site's `robots.txt` file for allowed pages. The application is designed to be user-friendly and versatile, enabling users to input any URL and automatically retrieve data from the pages that are permitted for web scraping.

## Features

- **URL Input**: Users can input any website URL.
- **Robots.txt Checking**: The app checks the `robots.txt` file of the provided URL to determine which pages are allowed for scraping.
- **Data Scraping**: Automatically scrapes allowed pages and retrieves basic data such as page title and content.
- **Data Display**: Scraped data is displayed in a tabular format using `pandas`.
- **CSV Download**: Users can download the scraped data as a CSV file.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/generalized-web-scraping-app.git
    cd generalized-web-scraping-app
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Enter the URL**: On the main page of the application, enter the URL of the website you want to scrape.
2. **Check Allowed Paths**: The app will check the `robots.txt` file of the website and display the allowed paths.
3. **Start Scraping**: Click the "Start Scraping" button to begin scraping the allowed pages.
4. **View and Download Data**: The scraped data will be displayed in a table, and you can download it as a CSV file.

## Example

If you input `https://books.toscrape.com/`, the application will:

1. Check the `robots.txt` file at `https://books.toscrape.com/robots.txt`.
2. Display the paths that are allowed for scraping.
3. Scrape the allowed pages and display the data such as page titles and content snippets.

## Project Structure

- `app.py`: The main Streamlit application file.
- `requirements.txt`: A list of required Python packages.
- `README.md`: This README file.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Issues and feature requests are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

This project uses the following open-source libraries:

- [Streamlit](https://streamlit.io/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [pandas](https://pandas.pydata.org/)
