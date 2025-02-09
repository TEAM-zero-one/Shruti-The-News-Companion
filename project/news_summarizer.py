from transformers import BartForConditionalGeneration, BartTokenizer
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import download
from typing import List, Optional
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

MODEL_NAME = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

def chunk_text(text: str, max_tokens: int = 900) -> List[str]:
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(tokenizer.tokenize(sentence))
        if current_length + sentence_length > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def summarize_chunk(chunk: str, **generate_kwargs) -> str:
    try:
        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
            padding="max_length"
        )
        summary_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            **generate_kwargs
        )
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error summarizing chunk: {str(e)}")
        return ""
    
def fix_punctuation(text: str) -> str:
    """
    Fix stray punctuation such as a comma immediately followed by a period or vice versa.
    """
    # Remove comma followed by period (and any spaces in between)
    text = re.sub(r",\s*\.", ".", text)
    # Remove period followed by comma
    text = re.sub(r"\.\s*,", ".", text)
    # Optionally, collapse multiple spaces into one
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def truncate_summary(full_summary, max_summary_length):
    if len(full_summary) <= max_summary_length:
        return full_summary.strip()
    
    sentences = sent_tokenize(full_summary)
    truncated = []
    current_length = 0
    
    for sent in sentences:
        # Determine the extra space needed: if truncated is not empty, add 1 for the space.
        spacer = 1 if truncated else 0  
        l = len(sent)
        if current_length + spacer + l <= max_summary_length:
            truncated.append(sent)
            current_length += spacer + l
        else:
            # If nothing has been added yet, just add the sentence regardless.
            if not truncated:
                truncated.append(sent)
            else:
                # Option 1: Do not add the sentence.
                diff_without = max_summary_length - current_length
                # Option 2: Add the full sentence.
                new_length_with = current_length + spacer + l
                diff_with = new_length_with - max_summary_length
                # Choose the option that gets closer to max_summary_length.
                if abs(diff_with) < abs(diff_without):
                    truncated.append(sent)
                    current_length = new_length_with
            break
                
    return ' '.join(truncated).strip()



def text_summarizer(
    text: str,
    min_len: Optional[int] = None,
    max_len: Optional[int] = None,
    quality_level: int = 4,
    detail_level: float = 2.0,
    repetition_control: float = 1.2,
    max_summary_length: int = 310,
    **kwargs
) -> str:
    if not text.strip():
        return "Input text is empty"
    
    # Calculate word count and set dynamic defaults
    word_count = len(word_tokenize(text))
    
    # Dynamic length adjustment based on input size
    if word_count < 1024:
        dyn_min, dyn_max = 50, 150
    elif 1024 <= word_count < 3000:
        dyn_min, dyn_max = 40, 100
    else:
        dyn_min, dyn_max = 30, 80
    
    # Using user parameters if provided, else dynamic values
    final_min = min_len if min_len is not None else dyn_min
    # final_max = max_len if max_len is not None else dyn_max
    final_max = dyn_max # temproary removed it because i want max_len to be max_summary_length

    max_summary_length = max_len if max_len is not None else max_summary_length
    
    # Ensuring valid length constraints
    final_min = max(10, min(final_min, 500))
    final_max = max(final_min + 20, min(final_max, 1000))
    
    generate_params = {
        'min_length': final_min,
        'max_length': final_max,
        'num_beams': quality_level,
        'length_penalty': detail_level,
        'repetition_penalty': repetition_control,
        'no_repeat_ngram_size': 3,
        **kwargs
    }
    
    # Split and process text
    chunks = chunk_text(text)
    summaries = [summarize_chunk(chunk, **generate_params) for chunk in chunks]
    
    # Post-process combined summary
    full_summary = ' '.join(
        sent.strip().capitalize() 
        for sent in sent_tokenize(' '.join(summaries))
        if sent.strip()
    )

    # Enforce hard length limit with sentence preservation

    full_summary = truncate_summary(full_summary, max_summary_length)
    full_summary = fix_punctuation(full_summary)
    return full_summary.strip()
