
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


llama_llama.py refers to the two llama models for processing text before and after. openai_openai.py refers to the two gpt models for processing text before and after.
before any openai model(gpt4, gpt4o), you need set up OPENAI_API_KEY=xxxxxx upfront.


    .
    ├── install.sh             # Environment setup script
    ├── README.md               # Readme file
    ├── s1                     # submission one files
    ├── s2                     # submission two files
    └── s2/report_of_S2.pdf    # report of submission two
