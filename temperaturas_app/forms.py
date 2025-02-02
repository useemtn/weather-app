from django import forms

class BuscarPaisForm(forms.Form):
    """
    
    Formulario para buscar un pais
    
    """
    nombre_pais = forms.CharField(label='Nombre del país', max_length=255)