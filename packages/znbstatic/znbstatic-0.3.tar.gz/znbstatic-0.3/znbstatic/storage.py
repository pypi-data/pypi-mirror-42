from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.deconstruct import deconstructible
from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage
from znbstatic.utils import add_version_to_url


@deconstructible
class VersionedStaticFilesStorage(StaticFilesStorage):
    """
    A static file system storage backend that appends
    the value from the ZNBSTATIC_VERSION setting.

    The storage class must be deconstructible.
    See `<https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/>`_.
    """
    def url(self, name):
        url = super(VersionedStaticFilesStorage, self).url(name)
        version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
        return add_version_to_url(url, version)


@deconstructible
class VersionedS3StaticFilesStorage(S3Boto3Storage):
    """
    A static file system storage backend that stores files on Amazon S3 and
    appends the value from the ZNBSTATIC_VERSION setting.

    The storage class must be deconstructible.
    See `<https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/>`_.

    Using bucket_name attribute to override default AWS_STORAGE_BUCKET_NAME setting.
    See S3Boto3Storage for other available attributes.
    """

    bucket_name = getattr(settings, 'AWS_STORAGE_STATIC_BUCKET_NAME', '')

    def url(self, name):
        url = super(VersionedS3StaticFilesStorage, self).url(name)
        version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
        return add_version_to_url(url, version)

# TODO for media and private

# class S3MediaStorage(S3Boto3Storage):
# 	"""
# 	Media files stored on Amazon S3.
# 	See storages.backends.s3boto.S3BotoStorage for other attributes.
# 	Requires AWS_STORAGE_MEDIA_BUCKET_NAME setting.
# 	"""
# 	bucket_name = getattr(settings, 'AWS_STORAGE_MEDIA_BUCKET_NAME', '')
#
# class S3PrivateStorage(S3BotoStorage):
# 	"""
# 	Private files stored on Amazon S3.
# 	See storages.backends.s3boto.S3BotoStorage for other attributes.
# 	Requires AWS_STORAGE_PRIVATE_BUCKET_NAME setting.
# 	"""
# 	bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME', '')
#

# From older znbdownload
# from storages.backends.s3boto import S3BotoStorage
# 
# from django.contrib.staticfiles.storage import StaticFilesStorage
# from django.conf import settings
# from django.utils.six.moves.urllib.parse import parse_qs
# from django.utils.six.moves.urllib.parse import urlencode
# 
# class VersionedS3StaticStorage(S3BotoStorage):
# 	"""
# 	Versioning for static files stored on Amazon S3.
# 	See storages.backends.s3boto.S3BotoStorage for other attributes.
# 	Requires ZNBCACHE_STATICFILES_VERSION setting.
# 	Requires AWS_STORAGE_STATIC_BUCKET_NAME setting.
# 	"""
# 	bucket_name = getattr(settings, 'AWS_STORAGE_STATIC_BUCKET_NAME', '')
# 
# 	def url(self, name):
# 		# if there is a query string already, isolate it
# 		try:
# 			idx = name.index('?')
# 			qs = name[idx+1:]
# 			name = name[:idx]
# 		except ValueError:
# 			idx = -1
# 			qs = None
# 
# 		# build a dictionary
# 		query = parse_qs(qs) if qs else {}
# 		query['v'] = getattr(settings, 'ZNBCACHE_STATICFILES_VERSION', '0.0')
# 		url = super(VersionedS3StaticStorage, self).url(name)
# 		static_cdn_url = getattr(settings, 'STATIC_CDN_URL', '')
# 		if static_cdn_url:
# 			url = url.replace((getattr(settings, 'STATIC_URL', '')), static_cdn_url)
# 		# rebuild query string and return versioned url
# 		qs = urlencode(query, doseq=True)
# 		return url + '?' + qs
# 
# class S3MediaStorage(S3BotoStorage):
# 	"""
# 	Media files stored on Amazon S3.
# 	See storages.backends.s3boto.S3BotoStorage for other attributes.
# 	Requires AWS_STORAGE_MEDIA_BUCKET_NAME setting.
# 	"""
# 	bucket_name = getattr(settings, 'AWS_STORAGE_MEDIA_BUCKET_NAME', '')
# 
# class S3PrivateStorage(S3BotoStorage):
# 	"""
# 	Private files stored on Amazon S3.
# 	See storages.backends.s3boto.S3BotoStorage for other attributes.
# 	Requires AWS_STORAGE_PRIVATE_BUCKET_NAME setting.
# 	"""
# 	bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME', '')
# 
# class VersionedStaticFilesStorage(StaticFilesStorage):
#     """
#     Versioning for static files.
# 
#     Requires ZNBCACHE_STATICFILES_VERSION setting.
#     """
# 
#     def url(self, name):
#         # if there is a query string already, isolate it
#         try:
#             idx = name.index('?')
#             qs = name[idx+1:]
#             name = name[:idx]
#         except ValueError:
#             idx = -1
#             qs = None
# 
#         # build a dictionary
#         query = parse_qs(qs) if qs else {}
#         query['v'] = getattr(settings, 'ZNBCACHE_STATICFILES_VERSION', '0.0')
#         url = super(VersionedStaticFilesStorage, self).url(name)
#         # rebuild query string and return versioned url
#         qs = urlencode(query, doseq=True)
#         return url + '?' + qs
