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
    set_name = request.GET.get('set_name') if request.method == 'GET' else request.POST.get('set_name')

    set_obj = FlashcardSet.objects.filter(name=set_name).first()
    if not set_obj:
        messages.error(request, 'Set not found')
        return redirect('read_sets')

    cards = Flashcard.objects.filter(set=set_obj)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')

        if not new_name.strip():
            messages.error(request, 'Name cannot be empty')
            return redirect(f'/seturi/set/edit/?set_name={set_name}')

        if FlashcardSet.objects.filter(name__iexact=new_name).exclude(pk=set_obj.pk).exists():
            messages.error(request, 'Name already exists')
            return redirect(f'/seturi/set/edit/?set_name={set_name}')

        set_obj.name = new_name
        set_obj.save()

        for card in cards:
            if request.POST.get(f"delete_{card.id}"):
                card.delete()
                continue

            q = request.POST.get(f"question_{card.id}")
            a = request.POST.get(f"answer_{card.id}")

            if q and a:
                card.question = q
                card.answer = a
                card.save()

        new_questions = request.POST.getlist('new_question')
        new_answers = request.POST.getlist('new_answer')

        for q, a in zip(new_questions, new_answers):
            if q.strip() and a.strip():
                Flashcard.objects.create(set=set_obj, question=q, answer=a)

        messages.success(request, 'Set updated successfully')
        return redirect('view_set')

    return render(request, 'seturi/edit_set.html', {
        "set": set_obj,
        "cards": cards
    })

def delete_set(request):
    if request.method == 'POST':
        set_name = request.POST.get('set_name')
        set_obj = get_object_or_404(FlashcardSet, name=set_name)
        set_obj.delete()
        messages.success(request, f'Set {set_name} was deleted successfully.')
        return redirect('read_sets')
    sets = FlashcardSet.objects.all()
    return render(request, 'seturi/delete_set.html', {'sets': sets})

def view_set(request):
    set_name = request.GET.get('set_name') or request.GET.get('set_name')

    if not set_name:
        messages.error(request, 'No set selected.')
        return redirect('read_sets')

    set_obj = get_object_or_404(FlashcardSet, name=set_name)
    cards = Flashcard.objects.filter(set=set_obj)

    return render(request, 'seturi/view_set.html', {"set": set_obj, "cards": cards})