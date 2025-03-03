
# LLM Normalization Toolkit

## Environment Requirements
- **Recommended OS**: Ubuntu 20.04 LTS (fully tested)
- **Minimum Python Version**: 3.6
- **Other Systems**: Partially supported, compatibility not guaranteed

## 📦 Installation Guide
    bash install.sh
# if your system is not ubuntu20.04, you can force script to install but we are not sure it can correctly run in your system

## How to run?
# Create result container file
touch code_like.txt

# Execute processor
python3 nor_code_like.py


This command is run directly in code like mode. Note that you need to create the corresponding file before running the Python script.

.
├── install.sh             # Environment setup script

├── nor_*.py               # Method entry files

├── train_eng.csv          # Input dataset

├── requirements.txt       # Python dependencies

└── *.txt                  # Auto-generated result files

└── report_1.pdf           # report about this project and method and data

└── code_description       # The Python code structure description, function by function
