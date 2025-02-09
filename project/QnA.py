from transformers import pipeline
def answers(context, question):
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        result = qa_pipeline({
                    'context': context,  # Using full article content or fallback to summary
                    'question': question
                })
        return result['answer']

