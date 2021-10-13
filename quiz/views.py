import random
import requests

from django import forms
from django.views.generic import FormView
from django.core.exceptions import ValidationError
from django.urls import reverse


CAPITALS_CACHE = None


def populate_cache():
    global CAPITALS_CACHE
    resp = requests.get("https://countriesnow.space/api/v0.1/countries/capital")
    CAPITALS_CACHE = {entry["name"]: entry["capital"] for entry in resp.json()["data"]}
    return CAPITALS_CACHE


class CapitalForm(forms.Form):
    country = forms.CharField()
    capital = forms.CharField()

    def is_valid(self):
        if CAPITALS_CACHE is None:
            capitals = populate_cache()
        else:
            capitals = CAPITALS_CACHE
        # run data cleaning
        super().is_valid()
        country = self.cleaned_data["country"]
        capital = self.cleaned_data["capital"]
        if capitals[country].casefold() != capital.casefold():
            self.add_error(
                "capital",
                ValidationError(f"The correct answer is: {capitals[country]}")
            )
        return super().is_valid()


class QuizView(FormView):
    template_name = "quiz.html"
    form_class = CapitalForm

    @staticmethod
    def _get_random_country():
        if CAPITALS_CACHE is None:
            capitals = populate_cache()
        else:
            capitals = CAPITALS_CACHE
        return random.choice(list(capitals))

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form["country"].field.widget.attrs["readonly"] = "readonly"
        return form

    def get_initial(self):
        return {
            "country": self._get_random_country()
        }

    def get_success_url(self):
        return f"{reverse('capitals_quiz')}?correct=1"

    def get(self, request, *args, **kwargs):
        correct = False
        if "correct" in request.GET:
            correct = True
        return self.render_to_response(self.get_context_data(correct=correct))

