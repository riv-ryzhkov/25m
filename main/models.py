from django.db import models


class Book(models.Model):
    title = models.CharField('Назва', max_length=50)
    author = models.CharField('Автор', max_length=50)
    text = models.TextField('Опис')
    published = models.CharField('Рік видання', max_length=4)
    count = models.IntegerField('Кількість', default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
