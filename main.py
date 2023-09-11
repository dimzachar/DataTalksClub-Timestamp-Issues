import json
from dotenv import load_dotenv
import os
from src.github_utility import GitHubUtility
from src.youtube_utility import YouTubeUtility
from src.transcript_processor import TranscriptProcessor
from src.processing_pipeline import ProcessingPipeline
def load_env_vars(var_names):
    """
    Load environment variables into a dictionary.
    
    :param var_names: List of environment variable names to load
    :return: Dictionary of environment variables
    :raises EnvironmentError: If any of the environment variables are not found
    """
    env_vars = {}
    for var in var_names:
        value = os.getenv(var)
        if value is None:
            raise EnvironmentError(f"{var} not found in environment variables")
        env_vars[var] = value
    return env_vars

def load_config(filename):
    """Load configuration from a JSON file.
    
    :param filename: Path to the JSON configuration file
    :return: Loaded JSON data
    """
    with open(filename, 'r') as f:
        return json.load(f)

def process_repositories(config, env_vars):
    """Process each repository based on the configuration and environment variables.
    
    :param config: Loaded JSON configuration
    :param env_vars: Loaded environment variables
    """
    for repo_config in config['repositories']:
        organization = repo_config['organization']
        repo_name = repo_config['repo_name']
        playlist_urls = repo_config['playlist_urls']
        
        print(f"Processing repository: {organization}/{repo_name}")

        github_util = GitHubUtility(env_vars['GITHUB_ACCESS_TOKEN'], f"{organization}/{repo_name}")

        for page in range(1, 3):
            print(f"Processing page {page} for issues...")
            
            video_titles = github_util.get_video_titles_from_issues(page)
            print(f"Video titles: {video_titles}")
            
            for playlist_url in playlist_urls:
                print(f"Processing playlist: {playlist_url}")

                youtube_util = YouTubeUtility(env_vars['YOUTUBE_API_KEY'], playlist_url)
                transcript_processor = TranscriptProcessor(env_vars['OPENAI_API_KEY'], repo_name=repo_name)
                
                pipeline = ProcessingPipeline(github_util, youtube_util, transcript_processor)
                pipeline.process_video(f"{organization}/{repo_name}", playlist_url, video_titles)



if __name__ == "__main__":
    """Main function to execute the processing pipeline."""
    
    print("Loading environment variables...")
    load_dotenv()
    env_vars_needed = ["YOUTUBE_API_KEY", "GITHUB_ACCESS_TOKEN", "OPENAI_API_KEY"]
    env_vars = load_env_vars(env_vars_needed)
    
    print("Loading JSON configuration...")
    config = load_config('config.json')
    
    print("Starting to process repositories...")
    process_repositories(config, env_vars)
