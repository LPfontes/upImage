from django.db import models

class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagens/')