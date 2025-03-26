
# LLM Normalization Toolkit

## Environment Requirements
- **Recommended OS**: Ubuntu 20.04 LTS (fully tested)
- **Minimum Python Version**: 3.6
- **Other Systems**: Partially supported, compatibility not guaranteed

## 📦 Installation Guide
    bash install.sh
if your system is not ubuntu20.04, you can force script to install but we are not sure it can correctly run in your system

## How to run?

Create result container file

cd s2 

touch xxxx.txt

### Execute processor

cd s2

python3 llama_llama.py

This command is run directly in code like mode. Note that you need to create the corresponding file before running the Python script.

llama_llama.py refers to the two llama models for processing text before and after. openai_openai.py refers to the two gpt models for processing text before and after.

.

├── install.sh             # Environment setup script

├── README.md               # Readme file

├── s1                     # submission one files

└── s2                     # submission two files
