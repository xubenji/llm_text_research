import matplotlib.pyplot as plt
import numpy as np

# Data for prompt group (including GPT4O and GPT4)
prompt_labels = ['key_drive', 'code_like', 'example_base', 'negative_positive', 'repeition_emphasie', 'GPT4O', 'GPT4']
prompt_scores = [0.2279, 0.2349, 0.2395, 0.2570, 0.2589, 0.2608, 0.2340]

# Data for model combination group
model_labels = ['llama3.3+llama3.3', 'GPT4O+GPT4O', 'GPT4+GPT4']
model_scores = [0.2191, 0.2602, 0.2241]

# Create x positions for both groups
x_prompts = np.arange(len(prompt_labels))
# Leave a gap between the two groups (choosing 1 unit here)
x_models = np.arange(len(model_labels)) + len(prompt_labels) + 1

plt.figure(figsize=(12, 6))

# Plot the bar chart for the prompt group
plt.bar(x_prompts, prompt_scores, color='skyblue', label='Prompts')

# Plot the bar chart for the model combination group
plt.bar(x_models, model_scores, color='salmon', label='Model Combinations')

# Combine the x-axis ticks and labels for both groups
all_x = np.concatenate([x_prompts, x_models])
all_labels = prompt_labels + model_labels
plt.xticks(all_x, all_labels, rotation=45)

plt.xlabel('Categories')
plt.ylabel('Score')
plt.title('Combined Median Scores for Prompts and Model Combinations')
plt.ylim(0.21, 0.30)
plt.legend()

plt.tight_layout()
plt.savefig('combined_results.png')
