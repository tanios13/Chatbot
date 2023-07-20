# College Chatbot
<!-- Prediction of Student Dropout -->
In this project, we implement chatbot trained on our own data (Admissions, Insitutions, Professional Insertion...). This chatbot answers any questions about these data.

## Installation
This shows how to setup the environement with anaconda to run the project

1. Clone the repo
```sh
git clone git@github.com:tanios13/Chatbot.git
```

2. Open the Anaconda Prompt, cd to the directory of the project and create a new env:
```sh
conda create --name myenv python=3.8
```

3. Install the list of required packages:
```sh
pip install -r requirements.txt
```

4. Install the package in editable mode (used to fix import from sibling folders):
```sh
pip install -e .
```

5. Export the OPENAI api key
```sh
conda env config vars set OPENAI_API_KEY=sky
conda deactivate env_name
conda activate env_name
```

6. Export the PINECONE api key
```sh
conda env config vars set PINECONE_API_KEY=sky
conda deactivate env_name
conda activate env_name
```

7. Use your new env as your python interpreter in your editor.