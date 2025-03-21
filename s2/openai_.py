import openai
import pandas as pd
from nltk.translate.meteor_score import meteor_score
from nltk import word_tokenize  # 导入分词器
import statistics
import os
import time

# 读取 CSV 文件（请替换为你的 CSV 文件路径）
df = pd.read_csv("train-eng.csv")

# 自定义 Prompts 模板（保持不变）
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
            "- If sentences are not English, please translate it into English.\n"
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
    使用 OpenAI API 对文本进行处理，生成摘要/标准化声明

    Args:
        api_key (str): OpenAI API 密钥
        text (str): 输入文本
        prompt_type (str): 使用的 prompt 模板，默认为 "repetition_emphasis"
        **kwargs: 可覆盖的额外模型参数

    Returns:
        str: 生成的文本
    """
    openai.api_key = api_key
    template = PROMPT_TEMPLATES.get(prompt_type, PROMPT_TEMPLATES["repetition_emphasis"])
    try:
        # 构建消息列表
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
        params.update(kwargs)  # 允许覆盖参数

        response = openai.ChatCompletion.create(**params)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API 调用失败: {str(e)}")
        print(f"sleep 60s!")
        time.sleep(60)  # 暂停程序 60 秒
        return claimed_text(api_key, text, prompt_type)

def read_file(file_path):
    """读取文本文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return None
    except Exception as e:
        print(f"读取文件失败: {str(e)}")
        return None

def get_score(references, candidate):
    """计算 METEOR 得分"""
    
    print(candidate)
    print(references)
    
    references = [references]
    tokenized_references = [word_tokenize(ref) for ref in references]
    tokenized_candidate = word_tokenize(candidate)
    score = meteor_score(tokenized_references, tokenized_candidate)
    return score

if __name__ == "__main__":
    output_file = "openai_4.result"
    # 初始化输出文件，写入标题行
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Index\tAvgScore\tScore\tNormalizedClaim\tText\n")
    except Exception as e:
        print(f"初始化输出文件失败: {str(e)}")

    # 检查 API 密钥（建议通过环境变量设置）
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

            # 第一步：调用 filter_1 模板进行预处理
            # text = claimed_text(API_KEY, input_text, prompt_type="filter_1")
            # print("After filter_1: " + str(text))
            # 第二步：调用 repetition_emphasis 模板进行标准化
            text = claimed_text(API_KEY, input_text, prompt_type="repetition_emphasis")
            prefix = "Standardized Claim: "
            # 方法1：直接切片（推荐，简洁高效）
            text = text[len(prefix):] if text.startswith(prefix) else text
            print("-" * 30)
            if text:
                score = get_score(normal_claim, text)
                scores.append(score)
                all_score += score
                avg_score = all_score / index
                print(f"{index}\tMETEOR Score: {score:.4f}\tAVG METEOR Score: {avg_score:.4f}")
                # 将结果追加写入文件
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{index}\t{avg_score:.4f}\t{score:.4f}\t{text}\t{normal_claim}\t\n")
            else:
                print("摘要生成失败")
        
        median_score = statistics.median(scores)
        # 更新文件第一行写入平均分和中位数分
        with open(output_file, "r+", encoding="utf-8") as f:
            original_content = f.read()
            f.seek(0, 0)
            f.write(f"avg_score:{avg_score:.4f}\tmedian_score:{median_score:.4f}\n")
            f.write(original_content)
