from django.db import models

# Create your models here.
from django.db import models


class Materia(models.Model):
    nome=models.CharField(max_length=100)
 
 
    
class Curso(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    materias=models.ManyToManyField(
        Materia,
        related_name="cursos"        
    )
    def __str__(self):
        return self.nome
class Cargo(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Lotacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Servidor(models.Model):
    nome=models.CharField(max_length=100)
    # não deixa apagar um cargos que ainda estão relacionado a um servidor 
    cargo=models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name="servidores"
    )

    lotacao=models.ForeignKey(
        Lotacao,
        on_delete=models.PROTECT,
        related_name='servidores'
    )
    cursos = models.ManyToManyField(
        Curso,
        related_name="servidores" )

    # cursos = models.ForeignKey(
    #     Curso,
    #     related_name="servidores",
    #     on_delete=models.PROTECT,
    # )

    def __str__(self):
        return self.nome
    

class Perfil(models.Model):
    servidor = models.OneToOneField(
        Servidor,
        on_delete=models.CASCADE,
        related_name="perfil"
    )
    bio = models.TextField()






class Nota(models.Model):
    valor=models.FloatField()
    materia=models.ForeignKey(
        Materia,
        related_name="notas",
        on_delete=models.CASCADE
    )
    servidor=models.ForeignKey(
        Servidor,
        related_name="notas",
        on_delete=models.CASCADE                
    )