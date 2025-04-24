import os
from together import Together

# 1. 确保用 Quickstart 文档要求的名字：
os.environ["TOGETHER_API_KEY"] = "ba668e3f782860d1d8c63778d34338a6b08b3f4af34f920e9f70c572d0f60d66"

# 2. 实例化时不传任何参数
client = Together()

# 3. 调用示例
messages = [
    {"role": "system",  "content": "你是一位友好的助手。"},
    {"role": "user",    "content": "你觉得下列帖子作者在隐喻什么？用一句话说 The salary of a U.S. Senator is $174,000 per year. This is Joe Biden’s house.... seems legit 🙄 "}
]

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=messages,
    max_tokens=4096,
    temperature=0.5,
    top_p=0.9,
    stop=["<|eot_id|>", "<|eom_id|>"]
)

print(response.choices[0].message.content)
