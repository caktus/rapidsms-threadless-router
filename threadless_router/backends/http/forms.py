from django import forms


class BaseHttpForm(forms.Form):

    def get_incoming_data(self):
        raise NotImplementedError()


class HttpForm(BaseHttpForm):

    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text')
        self.identity = kwargs.pop('identity')
        super(HttpForm, self).__init__(*args, **kwargs)
        self.fields[self.text] = forms.CharField()
        self.fields[self.identity] = forms.CharField()

    def get_incoming_data(self):
        return {'identity': self.cleaned_data[self.identity],
                'text': self.cleaned_data[self.text]}
