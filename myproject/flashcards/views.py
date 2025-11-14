from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.
from .models import FlashcardSet, Flashcard
from django import forms

predefined_sets = {
    "POO": {
        "title": "POO Basisc",
        "cards": [
            {"question": "Ce este un obiect?", "answer": "O instanta a unei clase."},
            {"question": "Ce este o clasa?", "answer": "Un sablon pentru crearea obiectelor."},
            {"question": "Ce este mostenirea", "answer": "Mecanismul prin care o clasa preia proprietati si metode din alta clasa."},
            {"question": "Ce este polimorfismul?", "answer": "Capacitatea aceleiasi metode de a se comporta diferit in functie de context."},
            {"question": "Ce este o interfata?", "answer": "Un tip care defineste doar metode fara implementare."},
            {"question": "Ce este overriding-ul?", "answer": "Redefinirea unei metode mostenite in clasa copil."},
            {"question": "Ce este overloading-ul?", "answer": "Definirea mai multor metode cu acelasi nume, dar parametri diferiti."}
        ]
    },
    "python": {
        "title": "Python Basics",
        "cards": [
            {"question": "Ce este o lista in Python?", "answer": "O colectie ordonata si modificabila de elemente."},
            {"question": "Ce este 'None'?", "answer": "O constanta care reprezinta absenta unei valori."},
            {"question": "Ce este un modul?", "answer": "Un fisier Python ce contine variabile, functii sau clase reutilizabile."},
            {"question": "Ce este un dictionar?", "answer": "O colectie de perechi cheie-valoare."},
            {"question": "Ce face functia pop()?", "answer": "Sterge si returneaza ultimul elemnet din lista."},
            {"question": "Ce tip de date returneaza functia input()?", "answer": "Intotdeauna un string."},
            {"question": "Ce este list comprehension?", "answer": "O metoda scurta de a crea liste folosind expresii."}
        ]
    },
    "cyber": {
        "title": "Cybersecurity",
        "cards": [
            {"question": "Ce este cybersecurity?", "answer": "Protejarea sistemelor si datelor impotriva atacurilor."},
            {"question": "Ce este un firewall?", "answer": "Un sistem care filtreaza traficul de retea."},
            {"question": "Ce este malware?", "answer": "Software malitios creat pentru a provoca daune"},
            {"question": "Ce este autentificare?", "answer": "Procesul prin care se verifica identitatea unui utilizator."},
            {"question": "Ce este un atac DDoS?", "answer": "Suprasolicitarea unui server cu trafic pentru a-l bloca."},
            {"question": "Ce este hashing-ul?", "answer": "Transformarea datelor intr-o valoare fixa, ireversibila."}
        ]
    },

    "so": {
        "title": "Sisteme de operare",
        "cards": [
            {"question": "Ce este un sistem de operare?", "answer": "Software care gestioneaza hardware-ul si ruleazaa aplicatiile."},
            {"question": "Ce este un thread?", "answer": "Cea mai mica unitate de executie dintr-un proces."},
            {"question": "Ce este memoria virtuala?", "answer": "Tehnica ce permite folosirea discului ca extensie a RAM-ului."},
            {"question": "Ce este kernel-ul?", "answer": "Componenta centrala a sistemului de operare."},
            {"question": "Ce este un deadlock?", "answer": "Situatie in care procesele se blocheaza reciproc."},
            {"question": "Ce este un sistem de fisiere?", "answer": "Structura prin care OS-ul organizeaza si stocheaza fisierele."}
        ]
    }

}

def predefined_list(request):
    return render(request, "seturi/predefined_sets.html", {
        "sets": predefined_sets
    })

def predefined_set(request, set_key):
    if set_key not in predefined_sets:
        return render(request, "seturi/predefined_sets.html", {
            "title": "Set not found",
            "cards": []
        })

    selected_set = predefined_sets[set_key]
    return render(request, "seturi/predefined_sets.html",{
        "title": selected_set["title"],
        "cards": selected_set["cards"],
    })



class FlashcardSetForm(forms.ModelForm):
    class Meta:
        model = FlashcardSet
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
                raise forms.ValidationError("The set name cannot be empty")

        existing = FlashcardSet.objects.filter(name__iexact=name)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError("Set name already exists")

        return name


def home(request):
    return render(request, 'seturi/home.html')

def create_set(request):
    if request.method == 'POST':
        form = FlashcardSetForm(request.POST)
        if form.is_valid():
            new_set = form.save()

            questions = request.POST.getlist('question')
            answers = request.POST.getlist('answer')

            for q, a in zip(questions, answers):
                if q.strip() and a.strip():
                    Flashcard.objects.create(set=new_set, question=q, answer=a)

            return redirect('read_sets')
    else:
        form = FlashcardSetForm()

    return render(request, 'seturi/create_set.html', {'form': form})


def read_sets(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'seturi/read_sets.html', {'sets': sets})


def edit_set(request):
    sets = FlashcardSet.objects.all()

    if request.method == 'POST':
        set_name = request.POST.get('set_name')
        new_name = request.POST.get('new_name')

        set_obj = FlashcardSet.objects.filter(name=set_name).first()
        if not set_obj:
            messages.error(request, 'Set not found')
            return redirect('create_set')

        if not new_name.strip():
            messages.error(request, 'New set name cannot be empty')
        elif FlashcardSet.objects.filter(name__iexact=new_name).exclude(pk=set_obj.pk).exists():
            messages.error(request, 'Set name already exists')
        else:
            set_obj.name = new_name
            set_obj.save()
            messages.success(request, f'Set \"{set_obj.name}\" was updated successfully')
            return redirect('read_sets')

    return render(request, 'seturi/edit_set.html', {'sets': sets})


def delete_set(request):
    if request.method == 'POST':
        set_name = request.POST.get('set_name')
        set_obj = get_object_or_404(FlashcardSet, name=set_name)
        set_obj.delete()
        messages.success(request, f'Set {set_name} was deleted successfully.')
        return redirect('read_sets')
    sets = FlashcardSet.objects.all()
    return render(request, 'seturi/delete_set.html', {'sets': sets})

