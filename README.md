# Documentation of LangChain
The primary goal of LangChain is to enable developers to build applications that can understand, generate, and interact with human-like text. We start by selecting one of the model provided by LangChain. Create prompts that serve as the input format to the language model. Once the input provided, we generate the response by sending the prompts to the language model. Depending on the model configuration, the model handle the response. 

## Model
The LangChain framework provides a standard interface to models: [Visit Models Documentation](https://python.langchain.com/en/latest/modules/models/getting_started.html):

1. LLMs: LLMs are designed to generate coherent and contextually relevant text based on a given prompt. LangChain provides wrappers for OpenAI, Cohere, Hugging Face... available in the __llms__ class. LangChain provide [documentation for these wrappers](https://python.langchain.com/en/latest/modules/models/llms/getting_started.html)

2. Chat Models: Chat models are specifically designed for conversational interactions. Unlike LLMs, chat models take into account the conversational context and history to generate contextually appropriate responses. LangChain provides wrappers for ChatOpenAI (gpt-3.5-turbo), googlePalm... available in the __chat_models__ class. LangChain provide [documentation for these wrappers](https://python.langchain.com/en/latest/modules/models/chat/getting_started.html)

3. Text Embedding Models: Text embedding model is convert text into a compact and dense numerical representation that captures the semantic meaning and relationships between words or documents, facilitating downstream NLP tasks. LangChain provides wrappers for OpenAI, Cohere, Hugging Face... available in the __embeddings__ class. LangChain provide [documentation for these wrappers](https://python.langchain.com/en/latest/modules/models/text_embedding.html)


## Prompts
Prompts refer to the input to the model. We generally use *PromptTemplate* [Visit Prompts Documentation](https://python.langchain.com/en/latest/modules/prompts.html).

The API provides __Selectors__ to choose which example to include in a prompt ([documentation](https://python.langchain.com/en/latest/modules/prompts/example_selectors.html)).

The API also provides __Output Parsers__ that help structure language model responses.([documentation](https://python.langchain.com/en/latest/modules/prompts/output_parsers.html)).

## Memory
You want the model to remember what was said before, especially when developping chatbots. LangChain provides an API and a guide to do that: [documentation](https://python.langchain.com/en/latest/modules/memory.html).

## Chains
It is the most important key block of LangChain. It combines a LLM with a template and we can combines these blocks together to carry on a sequence of operations on the data and lead to a step by step thinking of the model. Some of these chains models are:

1. LLM Chain: Basic chain techniques where we chain the prompt with the model. [See documentation](https://python.langchain.com/en/latest/modules/chains/getting_started.html)

2. Sequential Chains: Run chain one after the other. [See documentation](https://python.langchain.com/en/latest/modules/chains/generic/sequential_chains.html)

3. Router Chain: More complicated than the others. You built sub-chains each of which specialised for some input (can be classified depending on the subject). [See documentation](https://python.langchain.com/en/latest/modules/chains/generic/router.html)

4. Question Answering over documents: Answer question on a document and data which the model were not trained on, which makes it much more flexible. [See Documentation](https://python.langchain.com/en/latest/modules/chains/index_examples/question_answering.html)


## Callbacks and Evaluation
LangChain also provides an API to evaluate how the application is doing. [See Documentation](https://python.langchain.com/en/latest/modules/callbacks/getting_started.html)

## Agents
Some applications require not just a predetermined chain of calls to LLMs/other tools, but potentially an unknown chain that depends on the user’s input. In these types of chains, there is an [agent](https://python.langchain.com/en/latest/modules/agents.html) which has access to a suite of tools.