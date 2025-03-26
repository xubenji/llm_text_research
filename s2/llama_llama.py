from together import Together
from nltk.translate.meteor_score import meteor_score
from nltk import word_tokenize  # Import tokenizer
import statistics
import pandas as pd

import sys
import os

df = pd.read_csv("train-eng.csv")  # Replace with your CSV file path

# Custom prompt templates (remain unchanged)
PROMPT_TEMPLATES = {
    "filter_1": {
        "system": (
            "Please filter out the meaningless special symbols in the text and organize it into a complete sentence.\n"
            "Please give the filtering results directly without any explanation."
            "Make sure to keep the original meaning."
        ),
        "user_prefix": "Input: "
    },
    "repetition_emphasis": {
        "system": (
            "Your task is to convert user input into a standardized claim with one sentence. Ensure the following:\n"
            "- Make the statement more formal.\n"
            "- Avoid vague expressions.\n"
            "- Maintain correct grammar.\n"
            "- Ensure the output is a standardized claim with one sentence.\n"
            "Your task is to perform the same standardization process."
            "Extract the most brief information!"
        ),
        "user_prefix": "Please convert the following sentence into a standardized claim with one sentence: "
    },
}


def claimed_text(api_key, text, prompt_type="repetition_emphasis", **kwargs):
    """Summarize text using the Together API
    
    Args:
        api_key (str): Together API key
        text (str): The English text to be summarized
        prompt_type (str): Specify the prompt template to use, default is 'repetition_emphasis'
        **kwargs: Model parameters that can be overridden (e.g., temperature/max_tokens, etc.)
        
    Returns:
        str: The generated summary text
    """
    # Initialize the client
    client = Together(api_key=api_key)
    
    # Retrieve the prompt template
    template = PROMPT_TEMPLATES.get(prompt_type, PROMPT_TEMPLATES["repetition_emphasis"])
    # print(template)
    try:
        # Construct the list of messages
        messages = [
            {"role": "system", "content": template["system"]},
            {"role": "user", "content": template["user_prefix"] + text}
        ]
        
        # Merge default parameters with custom parameters
        params = {
            "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "messages": messages,
            "max_tokens": 3000,
            "temperature": 0.5,
            "top_p": 0.9,
            "stop": ["<|eot_id|>", "<|eom_id|>"],
            "stream": False
        }
        params.update(kwargs)  # Allow parameter override
        
        # Call the API
        response = client.chat.completions.create(**params)
        
        # Extract the result
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"API call failed: {str(e)}")
        return None


def read_file(file_path):
    """Read the contents of a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: File {file_path} does not exist")
        return None
    except Exception as e:
        print(f"File reading failed: {str(e)}")
        return None


def get_score(references, candidate):
    references = [references]
    tokenized_references = [word_tokenize(ref) for ref in references]
    tokenized_candidate = word_tokenize(candidate)
    print(references)
    print("------")
    print(candidate)
    # Calculate METEOR score
    score = meteor_score(tokenized_references, tokenized_candidate)
    return score


if __name__ == "__main__":

    output_file = "result_info.txt"
    # Initialize header (optional)
    try:
        with open(output_file, 'r+', encoding='utf-8') as f:
            f.write("Index\tAvgScore\tScore\tNormalizedClaim\tText\n")
    except FileExistsError:
        pass

    # Check API key (recommended to set via environment variable)
    API_KEY = os.getenv("TOGETHER_API_KEY")  # Prefer to read from environment variable
    if not API_KEY:
        API_KEY = "ba668e3f782860d1d8c63778d34338a6b08b3f4af34f920e9f70c572d0f60d66"  # Temporary test key
    
    if all(col in df.columns for col in ["post", "normalized claim"]):
        first_rows = df
        index = 0
        all_score = 0
        scores = []
        
        for index, row in first_rows.iterrows():
            index = index + 1
            print("=" * 50)
            # if index < 5630:
            #     continue
            input_text = row['post']
            normal_claim = row['normalized claim']
    
            # Generate and print summary
            text = claimed_text(API_KEY, input_text, prompt_type="filter_1")
            print("after filter1:" + str(text))
            text = claimed_text(API_KEY, str(text), prompt_type="repetition_emphasis")
            print("-" * 30)
            # prefix = "Here is the text organized into a complete sentence:"
            # # Method 1: Direct slicing (recommended, concise and efficient)
            # text = text[len(prefix):] if text.startswith(prefix) else text
            if text:
                score = get_score(normal_claim, text)
                # print(f"METEOR Score: {score:.4f}")
                scores.append(score)
                all_score = all_score + score
                avg_score = all_score / index
                print(f"{index}\tMETEOR Score: {score:.4f}\tAVG METEOR Score: {avg_score:.4f}")
                # Append directly
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{index}\t{avg_score:.4f}\t{score:.4f}\t{normal_claim}\t{text}\n")
            else:
                print("Summary generation failed")
        
        median_score = statistics.median(scores)
        # Open file in read/write mode (note: file must exist)
        with open(output_file, "r+", encoding="utf-8") as f:
            # Read the original content
            original_content = f.read()
            # Move to the beginning of the file
            f.seek(0, 0)
            # Write the formatted new content to the first line
            f.write(f"avg_score:{avg_score:.4f}\tmedian_score:{median_score:.4f}\n")
            # Write back the original content afterwards
            f.write(original_content)
