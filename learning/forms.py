from django import forms


class TestAttemptForm(forms.Form):
    """Форма будується динамічно під питання конкретного тесту."""

    def __init__(self, *args, test=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.test = test
        for question in test.questions.all():
            field_name = f'question_{question.id}'
            choices = [(a.id, a.text) for a in question.answers.all()]
            if question.question_type == question.MULTIPLE:
                self.fields[field_name] = forms.MultipleChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple,
                    required=False,
                )
            else:
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=False,
                )

    def score(self):
        """Повертає (score_percent: int, passed: bool)."""
        questions = list(self.test.questions.all())
        if not questions:
            return 0, False

        correct_count = 0
        for question in questions:
            field_name = f'question_{question.id}'
            correct_ids = set(
                str(a.id) for a in question.answers.filter(is_correct=True)
            )
            given = self.cleaned_data.get(field_name)
            if given is None:
                given_ids = set()
            elif isinstance(given, list):
                given_ids = set(given)
            else:
                given_ids = {given}

            if given_ids == correct_ids and given_ids:
                correct_count += 1

        score = round(correct_count / len(questions) * 100)
        passed = score >= self.test.passing_score
        return score, passed
