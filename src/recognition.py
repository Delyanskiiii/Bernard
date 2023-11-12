from vosk import Model, KaldiRecognizer

# model = Model(r"../model_small")
# recognizer = KaldiRecognizer(model, 96000)
# recognizer.SetWords(False)

def extract_text_between_second_quotes(input_string):
    first_quote_index = input_string.find('"')
    second_quote_index = input_string.find('"', first_quote_index + 1)
    third_quote_index = input_string.find('"', second_quote_index + 1)
    fourth_quote_index = input_string.find('"', third_quote_index + 1)
    
    if second_quote_index != -1:
        return input_string[third_quote_index + 1:fourth_quote_index]
    
    return None