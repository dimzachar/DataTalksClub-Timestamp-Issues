# DataTalksClub Timestamp Issues

## Description

This project automates the process of extracting transcripts from YouTube playlist videos that correspond to GitHub issues. It processes the transcripts to create timestamps and automatically adds them as comments to the relevant GitHub issues.

It is an extension of [this](https://github.com/dimzachar/Timecodes_issues_mlops), which was designed for MLOps Zoomcamp. I refactored and made it more modular to deal with all [DataTalksClub](https://github.com/DataTalksClub) courses and relevant playlists.

## Features

- Fetches YouTube video transcripts from specified playlists
- Matches videos with GitHub issues based on titles
- Processes transcripts to create timestamps
- Adds timestamps as GitHub issue comments

## Workflow

The script automates the process of generating timecodes for YouTube videos and adding them as comments to corresponding GitHub issues. Below is the sequence of steps that are executed:

1. **Load Environment Variables**: Essential API keys and tokens are loaded from environment variables.
   
2. **Load Configuration**: Configuration for repositories and playlists are loaded from a JSON file.

3. **GitHub Issues Fetching**: 
    - For each repository defined in the configuration, GitHub issues are fetched.
    - Only issues with a certain criteria (e.g., open state) are considered.

4. **YouTube Playlist Processing**:
    - For each YouTube playlist URL defined in the configuration, video details are fetched.
    - Videos matching the GitHub issues are identified.

5. **Transcript Processing**:
    - For each matching video, its transcript is fetched and processed.
    - Timecodes are generated based on the transcript.

6. **GitHub Commenting**:
    - A comment containing the timecodes is added to the corresponding GitHub issue.
    - If the issue already has a timecode comment, it is skipped.

7. **Error Handling**:
    - If transcripts are disabled or not found, an appropriate comment is added to the GitHub issue.
    - General exceptions are caught and logged, but the script continues with the next video or issue.


## Requirements

- Python 3.9 or higher
- GitHub Access Token
- YouTube API Key
- OpenAI API Key

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/dimzachar/DataTalksClub-Timestamp-Issues.git
    ```

2. Change directory:
    ```bash
    cd DataTalksClub-Timestamp-Issues
    ```

3. Install dependencies:
    ```bash
    pip install --upgrade pip
    pip install pipenv
    pipenv install --dev
    pipenv shell
    ```

4. Set up environment variables in a `.env` file:
    ```env
    YOUTUBE_API_KEY=your_youtube_api_key
    GITHUB_ACCESS_TOKEN=your_github_access_token
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

You can run the script and its associated quality checks and tests using a Makefile. The Makefile includes the following commands:

- `make test`: Run all unit tests using pytest. (TODO)
- `make quality_checks`: Perform quality checks using isort, black, and pylint.
- `make run`: Run tests, quality checks, and then the main script.

To run all of these sequentially, just use:

```bash
make run

## Cost Warning

Please note that using OpenAI's API key will incur costs. The script is configured to use OpenAI's GPT-3.5-turbo model by default, which is generally cheaper than text-davinci-003. You can easily switch to another model if you prefer.

## Contributing
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For inquiries, connect with me on [Linkedin](https://www.linkedin.com/in/zacharenakis/)
