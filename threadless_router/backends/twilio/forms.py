from django import forms


class TwilioForm(forms.Form):

    From = forms.CharField(max_length=16)
    Body = forms.CharField(max_length=160)

    def get_incoming_data(self):
        return {'identity': self.cleaned_data['From'],
                'text': self.cleaned_data['Body']}
