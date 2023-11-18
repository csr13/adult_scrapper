import os

def delete_object_from_media(obj):
    if os.path.exists(obj.image.path):
        os.unlink(obj.image.path)
    return True


def delete_all_images_from_blog(obj):
    for image in obj.images:
        delete_object_from_media(image)
    return True

