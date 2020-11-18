import os
import random

def handle_uploaded_file(f):  
    with open('media/attachment_records/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_products_file_path(instance, filename):

    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "attachment_records/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )