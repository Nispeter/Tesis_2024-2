

en_prompts = {
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
es_prompts = { 
    "context_query": """
        Use el contexto proporcionado para responder a la pregunta del usuario.\nNo puede responder a la pregunta del usuario a menos que haya un contexto específico en el texto siguiente.
        \n
        Si no puede responder la pregunta con el contexto, no sabe la respuesta o la pregunta no está relacionada con el contexto, responda con 'No se encontró contexto'.
        \n
        \n
        Contexto:\n
        {context}\n
        \n
        Pregunta:\n
        {question}\n"""
}
