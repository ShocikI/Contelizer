from django.shortcuts import render
from django.forms import Form, FileField
import random
import re
import chardet

class UpladFileForm(Form):
    file = FileField()


def shuffle_word(word: str) -> str:
    new_word = word
    if len(word) > 3:
        mid = list(word[1:-1])
        random.shuffle(mid)
        new_word = f"{word[0]}{''.join(mid)}{word[-1]}"
    return new_word

def change_text(text: str) -> str:
    # Pattern to pick whole word
    pattern = r'\b\w+\b'

    # Check whole text looking for pattern
    return re.sub(pattern, lambda word: shuffle_word(word.group()), text)

def upload_file_view(request):
    if request.method == 'POST':
        form = UpladFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            raw_data = uploaded_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

            try:
                text = raw_data.decode(encoding)
            except Exception as e:
                text = raw_data.decode(encoding, errors='replace')
            
            new_text = change_text(text)
            return render(
                request,
                'fileapp/result.html',
                {'new_text': new_text}
            )
    
    # GET
    form = UpladFileForm()
    return render(
        request, 
        'fileapp/upload.html', 
        {'form': form}
    )