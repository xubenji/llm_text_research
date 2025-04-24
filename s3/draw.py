import matplotlib.pyplot as plt

# Data
prompt_names = ['normal prompt', 'metaphor_prompts', 'photo_prompts', 'politics_prompts']
line_numbers = [654, 182, 215, 120]

# Create the plot
plt.figure(figsize=(6, 4))
plt.plot(prompt_names, line_numbers, marker='o', linestyle='-')
plt.xlabel('Prompt Type')
plt.ylabel('Line Number of Highest Score')
plt.title('Peak Line Numbers by Prompt Type')
plt.tight_layout()

# Save to PDF
plt.savefig('prompt_line_numbers.pdf')

