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
    scale = forms.ChoiceField(choices=BaseImagemForm.SCALES_CHOICES, required=True, label='Fator de Escala',widget=forms.Select(attrs={'id': 'id_scaleIA'}))
    model = forms.ChoiceField(choices=MODELS_CHOICES, required=True, label='Modelo de IA')
      # Desabilita o campo de escala
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se já tiver os dados do formulário (tipo num POST), ajusta a escala conforme o modelo
        model_value = self.data.get('model') or self.initial.get('model')
        if model_value == 'LapSRN':
            self.fields['scale'].choices = [('2', '2x'), ('4', '4x'), ('8', '8x')]
        else:
            self.fields['scale'].choices = [('2', '2x'), ('3', '3x'), ('4', '4x')]