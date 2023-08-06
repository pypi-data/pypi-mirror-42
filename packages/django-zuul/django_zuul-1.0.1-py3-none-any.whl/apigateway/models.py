import requests, json
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from uuid import uuid4


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apikey = models.CharField(max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.apikey is None:
            self.apikey = uuid4().hex
        super(Consumer, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username


class Api(models.Model):
    PLUGIN_CHOICE_LIST = (
        (0, 'Remote Auth'),
        (1, 'Basic Auth'),
        (2, 'Key Auth'),
        (3, 'Server Auth')
    )

    name = models.CharField(max_length=128, unique=True)
    request_path = models.CharField(max_length=255)
    upstream_url = models.CharField(max_length=255)
    plugin = models.IntegerField(choices=PLUGIN_CHOICE_LIST, default=0)
    consumers = models.ManyToManyField(Consumer, blank=True)

    def check_plugin(self, request):
        if self.plugin == 0:
            return True, ''
        elif self.plugin == 1:
            auth = BasicAuthentication()
            try:
                user, password = auth.authenticate(request)
            except:
                return False, 'Authentication credentials were not provided'

            if self.consumers.filter(user=user):
                return True, ''
            else:
                return False, 'Permission not Allowed'
        elif self.plugin == 2:
            apikey = request.META.get('HTTP_APIKEY')
            consumers = self.consumers.all()
            for consumer in consumers:
                if apikey == consumer.apikey:
                    return True, ''
            return False, 'Apikey Needed'
        elif self.plugin == 3:
            consumer = self.consumers.all()
            if not consumer:
                return False, 'consumer need'
            request.META['HTTP_AUTHORIZATION'] = requests.auth._basic_auth_str(consumer[0].user.username, consumer[0].apikey)
            return True, ''
        else:
            raise NotImplementedError('Plugin %d not implementd' % self.plugin)

    def send_request(self, request):
        headers = {}
        if self.plugin != 1 and request.META.get('HTTP_AUTHORIZATION'):
            headers['authorization'] = request.META.get('HTTP_AUTHORIZATION')
        # headers['content-type'] = request.content_type

        strip = '/service' + self.request_path
        full_path = request.get_full_path()[len(strip):]
        url = self.upstream_url + full_path
        method = request.method.lower()
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }

        for k, v in request.FILES.items():
            request.data.pop(k)

        if request.content_type and request.content_type.lower() == 'application/json':
            data = json.dumps(request.data)
            headers['content-type'] = request.content_type
        else:
            data = request.data

        return method_map[method](url, headers=headers, data=data, files=request.FILES)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
