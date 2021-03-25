from django.core.management.base import BaseCommand, CommandError
from donation_app.models import Institution, Category


class Command(BaseCommand):
    help = 'Creating exapmle foundations'

    def handle(self, *args, **options):
        try:
            cat1 = Category.objects.create(name='ubrania')
            cat2 = Category.objects.create(name='jedzenie')
            cat3 = Category.objects.create(name='sprzęt AGD')
            cat4 = Category.objects.create(name='meble')
            cat5 = Category.objects.create(name='zabawki')
            fund1 = Institution.objects.create(name='Przykladowa fundacja 1', description='Opis fundacji 1', type=1)
            fund1.category.set([cat4, cat1])
            fund1.save()
            fund2 = Institution.objects.create(name='Przykladowa fundacja 2', description='Opis fundacji 2', type=1)
            fund2.category.set([cat2, cat5])
            fund2.save()
            fund3 = Institution.objects.create(name='Przykladowa fundacja 3', description='Opis fundacji 3', type=1)
            fund3.category.set([cat1, cat2])
            fund3.save()
            fund4 = Institution.objects.create(name='Przykladowa fundacja 4', description='Opis fundacji 4', type=1)
            fund4.category.set([cat3, cat1])
            fund4.save()
            fund5 = Institution.objects.create(name='Przykladowa fundacja 5', description='Opis fundacji 5', type=1)
            fund5.category.set([cat4, cat5])
            fund5.save()
            fund6 = Institution.objects.create(name='Przykladowa fundacja 6', description='Opis fundacji 6', type=1)
            fund6.category.set([cat2, cat3])
            fund6.save()

            fund7 = Institution.objects.create(name='Przykladowa ngo 1', description='Opis fundacji 1', type=2)
            fund7.category.set([cat4, cat1])
            fund7.save()
            fund8 = Institution.objects.create(name='Przykladowa ngo 2', description='Opis fundacji 2', type=2)
            fund8.category.set([cat2, cat4])
            fund8.save()

            fund9 = Institution.objects.create(name='Przykladowa lokalna 1', description='Opis lokalnej 1', type=3)
            fund9.category.set([cat3, cat5])
            fund9.save()
            fund10 = Institution.objects.create(name='Przykladowa lokalna 2', description='Opis lokalnej 2', type=3)
            fund10.category.set([cat2, cat1])
            fund10.save()
            self.stdout.write(self.style.SUCCESS('Successfully added'))
        except:
            raise CommandError('Błąd dodawania')
