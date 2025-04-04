from together import Together
from nltk.translate.meteor_score import meteor_score
from nltk import word_tokenize  # 导入分词器
import statistics
import pandas as pd

import sys
import os

df = pd.read_csv("train-eng.csv")  # 替换为你的CSV文件路径

# 自定义Prompts模板（保持不变）
PROMPT_TEMPLATES = {
    "example_based": {
        "system": (
            "You are a language processing expert specializing in converting chaotic user statements into standardized claims with one sentence."
            "Here are some examples:\n"
            "- Input: 'A priceless clip of 1970 of Bruce Lee playing Table Tennis with his Nan-chak !! His focus on speed A priceless clip of 1970 of Bruce Lee playing Table Tennis with his Nan-chak !! His focus on speed A priceless clip of 1970 of Bruce Lee playing Table Tennis with his Nan-chak !! His focus on speed None' -> Standardized Claim: 'Late actor and martial artist Bruce Lee playing table tennis with a set of nunchucks.'\n"
            "- Input: 'Lieutenant Retired General Asif Mumtaz appointed as Chairman Pakistan Medical Commission PMC Lieutenant Retired General Asif Mumtaz appointed as Chairman Pakistan Medical Commission PMC Lieutenant Retired General Asif Mumtaz appointed as Chairman Pakistan Medical Commission PMC None' -> Standardized Claim: 'Pakistani government appoints former army general to head medical regulatory body.'\n"
            "Your task is to process new inputs in the same manner."
        ),
        "user_prefix": "Input: "
    },
    "code_like": {
        "system": (
            "Please use the following Jinja syntax to process chaotic input text and output a standardized normalized claim with one sentence:\n"
            "`{% normalize_claim(input_text) %}`\n"
            "Ensure that the statement is precise, concise, and follows formal written conventions."
        ),
        "user_prefix": "{% normalize_claim('"
    },
    "repetition_emphasis": {
        "system": (
            "Your task is to convert chaotic user input into a standardized claim with one sentence. Ensure the following:\n"
            "- Make the statement more formal.\n"
            "- Avoid vague expressions.\n"
            "- Maintain correct grammar.\n"
            "- Ensure the output is a standardized claim withe one sentence.\n"
            "Example:\n"
            "- 'The weather seems to be getting warmer' -> 'Data indicates an increase in temperature.'\n"
            "Your task is to perform the same standardization process."
        ),
        "user_prefix": "Please convert the following sentence into a standardized claim with one sentence: "
    },
    "negative_positive_instruction": {
        "system": (
            "Please standardize the user input without losing key information. For example:\n"
            "- 'I think this product is great' -> 'The user considers this product to be excellent.'\n"
            "Do **not** generate irrelevant content; only perform standardization."
        ),
        "user_prefix": "Input text: "
    },
    "keyword_driven": {
        "system": (
            "Please focus on the following keywords when performing standardization: 'data', 'evidence', 'research', 'observation', 'measurement'.\n"
            "If the input involves factual statements, reinforce its scientific nature. For example:\n"
            "- 'He might be sick' -> 'The person may be ill and requires further diagnosis.'\n"
            "Process the following input:"
        ),
        "user_prefix": "Input: "
    }
}


def claimed_text(api_key, text, prompt_type="example_based", **kwargs):
    """使用Together API进行文本总结
    
    Args:
        api_key (str): Together API密钥
        text (str): 需要总结的英文文本
        prompt_type (str): 指定使用的prompt模板，默认为'example_based'
        **kwargs: 可覆盖模型参数（如temperature/max_tokens等）
        
    Returns:
        str: 生成的摘要文本
    """
    # 初始化客户端
    client = Together(api_key=api_key)
    
    # 获取prompt模板
    template = PROMPT_TEMPLATES.get(prompt_type, PROMPT_TEMPLATES["example_based"])
    # print(template)
    try:
        # 构建消息列表
        messages = [
            {"role": "system", "content": template["system"]},
            {"role": "user", "content": template["user_prefix"] + text}
        ]
        
        # 合并默认参数与自定义参数
        params = {
            "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.5,
            "top_p": 0.9,
            "stop": ["<|eot_id|>", "<|eom_id|>"],
            "stream": False
        }
        params.update(kwargs)  # 允许覆盖参数
        
        # 调用API
        response = client.chat.completions.create(**params)
        
        # 提取结果
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return None


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
    references = [references]
    tokenized_references = [word_tokenize(ref) for ref in references]
    tokenized_candidate = word_tokenize(candidate)
    print(references)
    print("------")
    print(candidate)
    # 计算METEOR得分
    score = meteor_score(tokenized_references, tokenized_candidate)
    return score


if __name__ == "__main__":

    prompt_type = "code_like"
    output_file = prompt_type + ".txt"
    # 初始化标题（可选）
    try:
        with open(output_file, 'r+', encoding='utf-8') as f:
            f.write("Index\tAvgScore\tScore\tNormalizedClaim\tText\n")
    except FileExistsError:
        pass

     # 检查API密钥（建议通过环境变量设置）
    API_KEY = os.getenv("TOGETHER_API_KEY")  # 优先从环境变量读取
    if not API_KEY:
        API_KEY = "ba668e3f782860d1d8c63778d34338a6b08b3f4af34f920e9f70c572d0f60d66"  # 临时测试用
    
    if all(col in df.columns for col in ["post", "normalized claim"]):
        first_rows = df
        index = 0
        all_score = 5629 * 0.2592
        scores = []
        
        for index, row in first_rows.iterrows():
            index = index + 1
            print("=" * 50)
            if index < 5630:
                continue
            input_text = row['post']
            normal_claim = row['normalized claim']
    
            # 生成并打印摘要
            text = claimed_text(API_KEY, input_text, prompt_type=prompt_type)
            prefix = "Standardized Claim: "
            # 方法1：直接切片（推荐，简洁高效）
            text = text[len(prefix):] if text.startswith(prefix) else text
            if text:
                score = get_score(normal_claim, text)
                # print(f"METEOR Score: {score:.4f}")
                scores.append(score)
                all_score = all_score + score
                avg_score = all_score / index
                print(f"{index}\tMETEOR Score: {score:.4f}\tAVG METEOR Score: {avg_score:.4f}")
                    # 直接追加写入
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{index}\t{avg_score:.4f}\t{score:.4f}\t{normal_claim}\t{text}\n")
            else:
                print("摘要生成失败")
        
        median_score = statistics.median(scores)
        # 以读写模式打开文件（注意文件必须存在）
        with open(output_file, "r+", encoding="utf-8") as f:
            # 读取原有内容
            original_content = f.read()
            # 移动到文件开始位置
            f.seek(0, 0)
            # 写入格式化后的新内容到第一行
            f.write(f"avg_score:{avg_score:.4f}\tmedian_score:{median_score:.4f}\n")
            # 将原有内容写回到后面
            f.write(original_content)
