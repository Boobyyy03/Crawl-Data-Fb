# Facebook Post Crawler

This script allows you to log in to Facebook using your credentials stored in a text file and crawl the posts on your timeline. It utilizes Selenium, a web automation tool, to interact with the Facebook website.

## Prerequisites

- Python 3.x installed on your system.
- Chrome WebDriver installed. You can download it from [here](https://chromedriver.chromium.org/downloads) and ensure it's in your PATH.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/Boobyyy03/Crawl-Data-Fb.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Crawl-Data-Fb
    ```

3. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Add your Facebook login credentials to a text file named `fblogin.txt`. The file should contain two lines: your email/username on the first line and your password on the second line.

    Example `fblogin.txt`:
    ```
    your_email@example.com
    YourPassword123
    ```

2. Run the script:

    ```bash
    login_fb.py
    ```

3. The script will log in to Facebook using the provided credentials and start crawling the posts on your timeline. The posts will be saved to a file named `posts.txt` in the project directory.

## Notes

- Make sure to use this script responsibly and respect Facebook's terms of service.
- This script assumes that the Facebook login page and elements have static IDs. If Facebook updates its UI, the script may need adjustments.

