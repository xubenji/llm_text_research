import openai
import pandas as pd
from nltk.translate.meteor_score import meteor_score
from nltk import word_tokenize  # Import tokenizer
import statistics
import os
import time

# Read CSV file (please replace with your CSV file path)
df = pd.read_csv("train-eng.csv")

# Custom Prompts templates (remain unchanged)
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
            "You are a language expert and your task is to convert chaotic user input into a normalized claim. Ensure the following:\n"
            "- Avoid vague expressions.\n"
            "- Eliminate duplicate expressions.\n"
            "- If sentences are not English, please translate them into English.\n"
            "- Extract the most brief, useful, and meaningful information! This is most important!\n"
            "Here are some examples:\n"
            "- Input: 'A priceless clip of 1970 of Bruce Lee playing Table Tennis with his Nan-chak !! His focus on speed A priceless clip of 1970 of Bruce Lee playing Table Tennis with his Nan-chak !! His focus on speed A priceless clip of 1970 of Bruce Lee playing Table Tennis with his Nan-chak !! His focus on speed None' -> 'Late actor and martial artist Bruce Lee playing table tennis with a set of nunchucks.'\n"
            "- Input: 'Lieutenant Retired General Asif Mumtaz appointed as Chairman Pakistan Medical Commission PMC Lieutenant Retired General Asif Mumtaz appointed as Chairman Pakistan Medical Commission PMC Lieutenant Retired General Asif Mumtaz appointed as Chairman Pakistan Medical Commission PMC None' -> 'Pakistani government appoints former army general to head medical regulatory body.'\n"
        ),
        "user_prefix": "Please convert: "
    },
}

def claimed_text(api_key, text, prompt_type="repetition_emphasis", **kwargs):
    """
    Process text using the OpenAI API to generate a summary/standardized claim

    Args:
        api_key (str): OpenAI API key
        text (str): Input text
        prompt_type (str): The prompt template to use, default is "repetition_emphasis"
        **kwargs: Additional model parameters that can be overridden

    Returns:
        str: The generated text
    """
    openai.api_key = api_key
    template = PROMPT_TEMPLATES.get(prompt_type, PROMPT_TEMPLATES["repetition_emphasis"])
    try:
        # Construct the list of messages
        messages = [
            {"role": "system", "content": template["system"]},
            {"role": "user", "content": template["user_prefix"] + text}
        ]
        params = {
            "model": "gpt-4",
            "messages": messages,
            "max_tokens": 400,
            "temperature": 0.5,
            "top_p": 0.9,
            "stop": ["<|eot_id|>", "<|eom_id|>"],
        }
        params.update(kwargs)  # Allow parameter override

        response = openai.ChatCompletion.create(**params)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API call failed: {str(e)}")
        print("Sleeping for 60 seconds!")
        time.sleep(60)  # Pause the program for 60 seconds
        return claimed_text(api_key, text, prompt_type)

def read_file(file_path):
    """Read the content of a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: File {file_path} does not exist")
        return None
    except Exception as e:
        print(f"Failed to read file: {str(e)}")
        return None

def get_score(references, candidate):
    """Calculate the METEOR score"""
    
    print(candidate)
    print(references)
    
    references = [references]
    tokenized_references = [word_tokenize(ref) for ref in references]
    tokenized_candidate = word_tokenize(candidate)
    score = meteor_score(tokenized_references, tokenized_candidate)
    return score

if __name__ == "__main__":
    output_file = "openai_4.result"
    # Initialize the output file and write the header line
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Index\tAvgScore\tScore\tNormalizedClaim\tText\n")
    except Exception as e:
        print(f"Failed to initialize output file: {str(e)}")

    # Check API key (recommended to set via environment variable)
    API_KEY = os.getenv("OPENAI_API_KEY")

    if all(col in df.columns for col in ["post", "normalized claim"]):
        index = 0
        all_score = 0
        scores = []
        
        for _, row in df.iterrows():
            index += 1
            print("=" * 50)
            input_text = row['post']
            normal_claim = row['normalized claim']

            # Step 2: Call the repetition_emphasis template for standardization
            text = claimed_text(API_KEY, input_text, prompt_type="repetition_emphasis")
            prefix = "Standardized Claim: "
            # Method 1: Direct slicing (recommended, concise and efficient)
            text = text[len(prefix):] if text.startswith(prefix) else text
            print("-" * 30)
            if text:
                score = get_score(normal_claim, text)
                scores.append(score)
                all_score += score
                avg_score = all_score / index
                print(f"{index}\tMETEOR Score: {score:.4f}\tAVG METEOR Score: {avg_score:.4f}")
                # Append the results to the output file
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{index}\t{avg_score:.4f}\t{score:.4f}\t{text}\t{normal_claim}\t\n")
            else:
                print("Summary generation failed")
        
        median_score = statistics.median(scores)
        # Update the first line of the file with average and median scores
        with open(output_file, "r+", encoding="utf-8") as f:
            original_content = f.read()
            f.seek(0, 0)
            f.write(f"avg_score:{avg_score:.4f}\tmedian_score:{median_score:.4f}\n")
            f.write(original_content)
