RAG_prompts = {
    "context_query": """
        Use the provided context to answer the user's question.
        You may not answer the user's question unless there is specific context in the following text.
        If you cannot answer the question with the context, don't know the answer or the question is not related to the context, please respond with 'No context found'.
        \n
        \n
        Context:\n
        {context}\n
        \n
        Question:\n
        {question}\n
    """
}
emotional_prompts = {
    "classification_query":
        "Following the emotions: anticipation, joy, trust, fear, surprise, sadness, disgust, anger, none. "
        "Classify the emotion of the following dialogue and return only the word of the category without any other text: "
}

self_monitor_prompts = {
    "generate_summary":
        "Generate a new summary based on this information, maintaining continuity with previous summary."
}