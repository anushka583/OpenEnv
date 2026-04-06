tasks = [
    {
        "id": "easy",
        "query": "Summarize what Python is based on the document",
        "documents": [
            {"id": 1, "text": "Python is a widely used programming language known for simplicity and readability."}
        ],
        "reference_answer": "Python is a simple and widely used programming language."
    },
    {
        "id": "medium",
        "query": "Explain the difference between machine learning and deep learning",
        "documents": [
            {"id": 1, "text": "Machine learning involves algorithms that learn from data."},
            {"id": 2, "text": "Deep learning is a subset of machine learning using neural networks with multiple layers."}
        ],
        "reference_answer": "Deep learning is a subset of machine learning that uses neural networks."
    },
    {
        "id": "hard",
        "query": "Summarize the advantages and limitations of renewable energy",
        "documents": [
            {"id": 1, "text": "Renewable energy reduces pollution and dependence on fossil fuels."},
            {"id": 2, "text": "It can be expensive to set up and depends on environmental conditions."},
            {"id": 3, "text": "Sources like solar and wind are not always consistent."}
        ],
        "reference_answer": "Renewable energy reduces pollution but can be costly and inconsistent."
    }
]