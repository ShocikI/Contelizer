from django.shortcuts import render
from django.forms import Form, CharField

class PeselForm(Form):
    pesel = CharField(max_length=11, min_length=11, label="PESEL")

def validate_pesel(pesel: str) -> tuple:
    try:
        pesel_nums = [int(x) for x in pesel]
    except:
        return False, None, None
    
    weights = [1, 3, 7, 9, 1, 3, 7 ,9, 1, 3]
    checksum = sum(pesel_nums[i] * weights[i] for i in range(10))
    control_digit = (10 - (checksum % 10 )) % 10

    if control_digit != (pesel_nums[-1]):
        return False, None, None
    
    year = int(pesel[:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])
    gender = "Kobieta" if int(pesel[9]) % 2 == 0 else "Mężczyzna"

    if month > 80:
        year += 1800
        month -= 80
    elif month > 60:
        year += 2200
        month -= 60
    elif month > 40:
        year += 2100
        month -= 40
    elif month > 20:
        year += 2000
        month -= 20
    else: 
        year += 1900

    return True, f"{year}-{month:02d}-{day:02d}", gender

def pesel_view(request):
    result = None
    
    if request.method == "POST":
        form = PeselForm(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            valid, birth_date, gender = validate_pesel(pesel)
            result = {
                "valid": valid,
                "birth_date": birth_date,
                "gender": gender
            }
    # GET
    else:
        form = PeselForm()
    return render(
        request, 
        'peselapp/pesel.html',
        {
            'form': form, 
            'result': result
        }
    )