from django import forms


class QuestionImportForm(forms.Form):
    """Форма завантаження Excel-файлу з питаннями для конкретного тесту."""

    file = forms.FileField(
        label='Excel-файл (.xlsx)',
        help_text='Заповніть за шаблоном: колонки order, question_type, question, '
                   'answer_1, correct_1, answer_2, correct_2 ...',
    )
    replace_existing = forms.BooleanField(
        label='Видалити наявні питання цього тесту перед імпортом',
        required=False, initial=False,
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.lower().endswith('.xlsx'):
            raise forms.ValidationError('Потрібен файл у форматі .xlsx (Excel).')
        return file


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
