import re
import os
from datetime import timedelta

class TranscriptProcessor:
    """
    Class to process transcripts and generate timestamps.
    """

    def __init__(self, openai, repo_name):
        """
        Initialize the TranscriptProcessor.

        :param openai: OpenAI API client
        :param repo_name: Repository name to set as the output directory
        """
        self.openai = openai
        self.output_directory = repo_name
        os.makedirs(self.output_directory, exist_ok=True)

    def clean_text(self, text):
        """
        Clean text by removing timestamps.

        :param text: Text to clean
        :return: Cleaned text
        """
        return re.sub(r'(?<!^)(\d{1,2}:\d{2}:\d{2})|(\d{1,2}:\d{2})', '', text).strip()

    def process_chunk(self, current_text_chunk, chunk_start_time):
        """
        Process a chunk of transcript text.

        :param current_text_chunk: The current text chunk to process
        :param chunk_start_time: The start time of the chunk
        :return: Processed timestamp
        """
        prompt = f"Summarize the following in 6 words or less: '{current_text_chunk}'. Strict 6-word limit."
        messages = [{"role": "system", "content": "You are a YouTube video creator."},
                    {"role": "user", "content": prompt}]

        # Query OpenAI API for text summarization
        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50,
            n=1,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        
        description = self.clean_text(response.choices[0].message['content']).rstrip('.')
        timestamp_string = str(timedelta(seconds=int(chunk_start_time)))
        polished_timestamp = f"{timestamp_string} - {description}".replace("\n", " ").replace('"', '').replace(" - -", " -").rstrip('.')
        
        return polished_timestamp

    def process_transcript(self, whole_transcript, chunk_size):
        """
        Process an entire transcript.

        :param whole_transcript: The transcript to process
        :param chunk_size: Size of each chunk for processing
        :return: Processed transcript as a comment body
        """
        print("Sending data to OpenAI for processing...")
        
        current_text_chunk = ""
        comment_body = []
        chunk_start_time = 0

        print("Processing transcript...")
        for current_line in whole_transcript:
            if chunk_start_time == 0:
                chunk_start_time = current_line['start']
            
            current_text_chunk += " " + current_line['text']
            
            if len(' '.join(current_text_chunk).split(" ")) > chunk_size:
                polished_timestamp = self.process_chunk(' '.join(current_text_chunk), chunk_start_time)
                comment_body.append(polished_timestamp)
                
                chunk_start_time = 0
                current_text_chunk = ""
        
        # Save to output directory
        with open(f"{self.output_directory}/timestamps.txt", "a", encoding="utf-8") as file:
            file.write('\n'.join(comment_body) + '\n')

        return '\n'.join(comment_body)
