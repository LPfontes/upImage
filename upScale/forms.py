from django import forms
from .models import Imagem





class BaseImagemForm(forms.ModelForm):
    SCALES_CHOICES = [
        ('2', '2x'),
        ('3', '3x'),
        ('4', '4x')
    ]
    scale = forms.ChoiceField(choices=SCALES_CHOICES, required=True, label='Fator de Escala')
    class Meta:
        model = Imagem
        fields = ['imagem']


class ImagemForm(BaseImagemForm):
    INTERPOLATION_CHOICES = [
        ('Lanczos', 'Lanczos'),
        ('Linear', 'Linear'),
        ('Cubic', 'Cubic')
    ]
    interpolation = forms.ChoiceField(choices=INTERPOLATION_CHOICES, required=True, label='Algoritmo de Interpolação')

class ImagemFormIA(BaseImagemForm):
    MODELS_CHOICES = [
        ('EDSR', 'EDSR'),
        ('FSRCNN', 'FSRCNN'),
        ('ESPCN', 'ESPCN'),
        ('LapSRN', 'LapSRN'),
    ]
    model = forms.ChoiceField(choices=MODELS_CHOICES, required=True, label='Modelo de IA')
    