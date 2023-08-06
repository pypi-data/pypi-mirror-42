# -*- coding: utf-8 -*-


"""
filter :class:`s3.Object` or :class:`s3.ObjectSummary`.

s3 object has following attributes can be used for filtering:

- Object.bucket_name
- Object.key
- Object.e_tag
- Object.last_modified
- Object.size

reference: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#objectsummary
"""

from botocore.exceptions import ClientError


def get_obj_size(s3_obj):
    try:  # s3.ObjectSummary
        return s3_obj.size
    except:  # s3.Object
        return s3_obj.content_length


class FiltersConstructor(object):
    """
    Construct a ``s3.Object`` filter function.
    """

    @staticmethod
    def validate_method_type_args(is_classmethod, is_staticmethod, is_regularmethod):
        if sum([is_classmethod, is_staticmethod, is_regularmethod]) > 1:
            raise ValueError

    def by_extension(self,
                     ext,
                     case_sensitive=False,
                     is_classmethod=False,
                     is_staticmethod=False,
                     is_regularmethod=False):
        self.validate_method_type_args(
            is_classmethod, is_staticmethod, is_regularmethod)

        if case_sensitive:
            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return s3_obj.key.endswith(ext)
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return s3_obj.key.endswith(ext)
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return s3_obj.key.endswith(ext)
            else:
                def filters(s3_obj):
                    return s3_obj.key.endswith(ext)
        else:
            ext = ext.lower()

            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return s3_obj.key.lower().endswith(ext)
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return s3_obj.key.lower().endswith(ext)
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return s3_obj.key.lower().endswith(ext)
            else:
                def filters(s3_obj):
                    return s3_obj.key.lower().endswith(ext)
        return filters

    def by_basename(self,
                    basename,
                    case_sensitive=False,
                    is_classmethod=False,
                    is_staticmethod=False,
                    is_regularmethod=False):
        self.validate_method_type_args(
            is_classmethod, is_staticmethod, is_regularmethod)
        if case_sensitive:
            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
            else:
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
        else:
            basename = basename.lower()

            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
            else:
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
        return filters

    def by_last_modified_after(self, a_datetime):
        def filters(s3_obj):
            return s3_obj.last_modified >= a_datetime

        return filters

    def by_last_modified_before(self, a_datetime):
        def filters(s3_obj):
            return s3_obj.last_modified <= a_datetime

        return filters

    def by_last_modified_between(self, after, before):
        def filters(s3_obj):
            return after <= s3_obj.last_modified <= before

        return filters

    def by_md5(self, md5):
        def filters(s3_obj):
            return s3_obj.e_tag == md5

        return filters

    def by_size(self, min_size_in_bytes=-1, max_size_in_bytes=999999999999):
        def filters(s3_obj):
            size = get_obj_size(s3_obj)
            return min_size_in_bytes <= size <= max_size_in_bytes

        return filters


filter_constructor = FiltersConstructor()


class _Filters(object):
    """
    Pre-defined ``s3.Object`` filters.
    """

    def exists(self, obj):
        """
        Test if this object exists.
        """
        try:
            obj.e_tag
            return True
        except ClientError:
            return False
        except:
            return False

    def not_exists(self, obj):
        """
        Test if this object exists.
        """
        return not self.exists(obj)

    csv = filter_constructor.by_extension(".csv", case_sensitive=False)
    """Test if it is a ``.csv`` file"""

    json = filter_constructor.by_extension(".json", case_sensitive=False)
    """Test if it is a ``.json`` file"""

    gzip = filter_constructor.by_extension(".gz", case_sensitive=False)
    """Test if it is a ``.gz`` file"""

    log = filter_constructor.by_extension(".log", case_sensitive=False)
    """Test if it is a ``.log`` file"""


Filters = _Filters()


def select_from(objects, filters):
    for s3_obj in objects:
        if filters(s3_obj):
            yield s3_obj
