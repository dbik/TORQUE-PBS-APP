from rest_framework.views import exception_handler


def profile_image_path(instance, filename):
    path = 'media/%s/' % instance.username
    path = path + 'normal/' + '%s' % instance.profile_image
    print path
    return path


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response