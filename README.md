# Canada Immigration Tracker 🚀

This repository contains Python scripts for scraping immigration draw updates for the Ontario Immigrant Nominee Program (OINP) and Express Entry (EE). The project also includes a GitHub Actions workflow to automate the scraping process and send notifications via SMS through Twilio.

## Features ✨

- **OINP Draw Scraper**: Scrapes updates from the OINP website and sends SMS notifications for new draws. 📈
- **EE Draw Scraper**: Scrapes updates from the Express Entry draws page and sends SMS notifications for new draws. 📊
- **GitHub Actions Workflow**: Automates the scraping process and manages notifications based on a schedule or manual trigger. 🔄
- **Twilio Integration**: Notifications are sent via SMS texts through Twilio. 📱

## Relevant Files 📁

1. `oinpscraper.py`: Scrapes OINP draw updates. 📝
2. `eescraper.py`: Scrapes EE draw updates. 📝
3. `.github/workflows/poll.yml`: GitHub Actions workflow configuration. ⚙️

## Requirements 🛠️

- Python 3.x
- `requests` library (for OINP scraper)
- `beautifulsoup4` library
- `python-dotenv` library
- `twilio` library
- `selenium` library
- Google Chrome and ChromeDriver (for EE scraper)

## Installation 🛠️

1. Clone the repository:
    ```bash
    git clone https://github.com/A223D/canada-immigration-tracker.git
    cd canada-immigration-tracker
    ```

2. Install the required Python packages:

    ```bash
    pip install requests beautifulsoup4 python-dotenv twilio selenium
    ```

3. Set Up Environment Variables. Make sure to create the environment variables for recipient phone numbers and reference them in code. These variables are defined at the repository level on GitHub: Create a .env file in the root directory of the project with the following content:

    ```env
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    FROM_NUMBER=your_twilio_phone_number
    #create the environment variables for all recipients + add them to GitHub + reference them in code
    TEXT_TEST=true # set to 'false' for live mode
    SEND_TO=All # Options: "All" or "Just you"
    GITHUB_OUTPUT=path_to_github_output_file
    ```

4. ChromeDriver Setup: Ensure Google Chrome and ChromeDriver are installed and compatible with your Chrome version. 🌐

## Usage 🚀

Test Mode:
    Use local test files (prettyOINP.txt and prettyEE.txt) to simulate scraping.
    Set TEXT_TEST=true in the .env file. 🔍

Live Mode:
    The scripts will fetch the latest updates from the respective immigration websites.
    Ensure TEXT_TEST=false or remove the TEXT_TEST entry in the .env file. 🌟

Running the Scripts:
    Run the OINP scraper:

```bash
python oinp_scraper.py
```

Run the EE scraper:

```bash
python ee_scraper.py
```

## GitHub Actions Workflow 🔧

The workflow file .github/workflows/poll.yml is configured to run the scraping scripts every 4 hours. 🕓

There is a manual trigger with inputs for `text_test` and recipient choice for testing. 🚀

## To-Do ✅
Might be a good idea to integrate with the [`simple-github-announcements`](https://github.com/A223D/simple-github-announcements) project.

Can also look at scraping pages of other provinces, or selective notifications based on certain programs. 

## Contributing 🤝

Feel free to open issues or submit pull requests for improvements or bug fixes. Please ensure your code adheres to the existing style and includes tests where applicable.