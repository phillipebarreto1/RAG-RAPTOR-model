# Langchain RAG Tutorial

Install dependencies.

```python
pip install -r requirements.txt
```

Create the Chroma DB.

```python
python create_database.py
```

Query the Chroma DB.

```python
python query_data.py "How does Alice meet the Mad Hatter?"
```

You'll also need to set up an OpenAI account (and set the OpenAI key in your environment variable) for this to work.
export openai_api_key=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
export OPENAI_API_KEY=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

ball dont lie api = f67151cc-842a-480c-9374-77a08265fb0f