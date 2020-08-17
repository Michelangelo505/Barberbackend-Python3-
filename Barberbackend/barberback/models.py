from django.db import models
from django.contrib.auth.models import User
from .compress import *
from django.conf import settings
import uuid
# Create your models here.


class BarberProfile(models.Model):
    class Meta:
        db_table = 'barber_profile'

    Barber_Phone = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='Телефон пользователя')
    Barber_User = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return '%s %s' % (self.Barber_User, self.Barber_Phone)


class BarberService(models.Model):
    class Meta:
        db_table = 'barber_service'

    bService = models.CharField(max_length=200, verbose_name='Наименование услуги')
    bPrice = models.DecimalField(verbose_name='Цена услуги', max_digits=15, decimal_places=2)
    bService_text = models.TextField(verbose_name='Описание услуги', blank=True)

    def __str__(self):
        return 'Услуга: %s  Цена: %s' % (self.bService, self.bPrice)


class BarberNews(models.Model):
    def upload_file(instance,filename,upload_dir='imgnews',ext='png'):
        """
        Генерирует путь куда будут загружаться картинки,при этом
        изменяется имя файла и его расширение

        :param filename: имя файла
        :param upload_dir: директория куда будут загружаться файлы
        :param ext: расшерение картинки
        :return: возращает путь к файлу
        """
        without_ext_filename = filename.split('.')[0] + '_'+ uuid.uuid4().hex
        return f'{upload_dir}/{without_ext_filename}.{ext}'

    class Meta:
        db_table = 'barber_news'
        ordering = ['bNewsDate']

    bTitleNews = models.CharField(max_length=150, verbose_name='Заголовок')
    bTextNews = models.TextField(verbose_name='Текст новости')
    bNewsDate = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    bNewsImage = models.ImageField(upload_to=upload_file, verbose_name='Картинка новости', blank=True)

    def save(self, *args, **kwargs):
        super(BarberNews, self).save(*args, **kwargs)

    def __str__(self):
        return 'Дата создания: %s  Заголовок новости: %s' % (self.bNewsDate, self.bTitleNews)

    def ChangeImage(self):
        """
        Изменяет полученную картинку: сохраняет в формате,указанном в расширении файла
        и масштабирует

        :return: None
        """
        width = 512
        height = 512
        result = CompressImage(settings.MEDIA_ROOT + str(self.bNewsImage),width,height)
        # Пока вывожу информацию обработки в консоль.
        # В идеале нужно в лог-файл !
        if result:
            print(f'Обработка изображения - {str(self.bNewsImage)} произошла успешно')
        else:
            print(f'Ошибка в обработке изображения - {str(self.bNewsImage)} !')

class BarberUserSendNews(models.Model):
    class Meta:
        db_table = 'barber_sendNews'

    bNewsUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bNewsUser')
    bNews = models.ForeignKey(BarberNews, on_delete=models.CASCADE, related_name='bNews')
    bSend = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.bNewsUser, self.bNews.bTitleNews, self.bSend)


class ServiceTime(models.Model):
    class Meta:
        db_table = 'barber_service_time'
        ordering = ['bTime']

    bTime = models.TimeField(verbose_name='Время услуги')
    bTimeStatus = models.CharField(max_length=10, verbose_name='СлужебноеПоле', blank=True, editable=False)

    def __str__(self):
        return 'Время Услуги: %s ' % (self.bTime)


class BarberMasters(models.Model):
    class Meta:
        db_table = 'barber_masters'

    bMaster = models.CharField(max_length=100, verbose_name='Фамилия или Имя или Ник')
    bMaster_text = models.TextField(verbose_name='Описание мастера', blank=True, )
    bDateBegin = models.DateField(verbose_name='Служебное поле дата начала отсутствия', blank=True, null=True,
                                  editable=False)
    bDateEnd = models.DateField(verbose_name='Служебное поле дата окончания отсутствия', blank=True, null=True,
                                editable=False)

    def __str__(self):
        return 'Мастер: %s ' % (self.bMaster)


class UserOrders(models.Model):
    """  Таблица заявок пользователей """

    class Meta:
        db_table = 'barber_user_orders'
        ordering = ['bOrderCreateDate']

    bOrderService = models.ForeignKey(BarberService, on_delete=models.CASCADE, related_name='relOrderService')
    bOrderUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relOrderUser')
    bOrderMaster = models.ForeignKey(BarberMasters, on_delete=models.CASCADE, related_name='relOrderMaster')
    bOrderCreateDate = models.DateField(verbose_name='Дата создания')
    bOrderTimeService = models.ForeignKey(ServiceTime, on_delete=models.CASCADE, related_name='relOrderServiceTime')
    bOrderStatus = models.BooleanField(default=False)

    def __str__(self):
        return 'Дата создания: %s  Клиент: %s  %s  %s  %s ' % (
        self.bOrderCreateDate, self.bOrderUser, self.bOrderMaster, self.bOrderService, self.bOrderTimeService)


'''
class PushUserOrder(models.Model):
    class Meta:
        db_table = 'barber_pushuserorder'        

    bPushUser    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relPushUser')    
'''


class MasterTimeTable(models.Model):
    """ Таблица расписания мастеров записи редактируются Администратором """

    class Meta:
        db_table = 'master_time'

    bTimeMaster = models.ForeignKey(BarberMasters, on_delete=models.CASCADE, related_name='reltimemaster')
    bDateBegin = models.DateField(verbose_name='Дата начала отсутствия')
    bDateEnd = models.DateField(verbose_name='Дата окончания отсутствия')

    def __str__(self):
        return 'Мастер: %s Отсутствует от %s до %s ' % (self.bTimeMaster, self.bDateBegin, self.bDateEnd)