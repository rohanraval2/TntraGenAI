# TntraGenAI

# File explanation

The DemoRun.ipynb file contains every code and file merged together

## PyTorch Model
    Training Model code is in TorchModelTraining.ipynb
    Load 1 or multiple dataframes or .xlsx files (created by SuperHelperForTrainData.py) and adjust the number of epochs according to the data.
    Training happens in batches hence large amount of data can be used for training

    Save your model in a .pth file

    Model predicition code is also present   

## Helper Classes and .py files
    1. SuperHelperForTrainData.py 
        -> Input : directory to pdf file. 
        -> Output : it makes a dataframe where each line in the pdf, with their font_size, and bold is recorded
        -> This file can be used for both for training data, and also while using the Model 
    
    2. TopicContentRelater.py
        -> This is used after the model has predicted
        -> Input : Takes a pandas DataFrame/ .xlsx/ or .csv file which has the data of the predicted texts
        -> Output : Outputs a dictionary with Topic/ Title as their key and their respective Content as the values. Values of the dict are in a list. Also gives output of the title and their subtitle
    
    3. GenAI.py
        -> Uses Gemini 1.0 or OpenAI ChatGPT 4o Mini (paid) API to generate the explanation and the questions
        -> Prompt can be re-engineered. To use less tokens per request - you can use summarizing HuggingFace model to summarize the content for each title to use less limit. 
        -> Input : Title, and Content
        -> Output : Generated output for each title, and content (hence it has to be saved in a datatype on your end)

    4. MarkDownConverter.py
        -> Converts the written content from GenAI to a combined HTML file
        (This needs edit since there are formatting issues in the HTML)
    
## Integrating

    This can be integrated from GenAI part and onwards. Once the GenAI has generated text based on the prompt and the input title and content, it can be used and displayed for any use. Export the datatype to your location and it can be printed or displayed from there own.
