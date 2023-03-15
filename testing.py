import boto3
import os
from werkzeug.utils import secure_filename

#aws
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

image = open('static/avacado.jpg').read()
s3.upload_fileobj(image, os.getenv("AWS_BUCKET_NAME"), 'avacado.jpg', ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": 'jpg'
                })
#Methods
def handleImage(image):
    if image:
        filename = secure_filename(image.filename)
        try:
            s3.upload_fileobj(
                image,
                os.getenv("AWS_BUCKET_NAME"),
                filename,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": image.content_type
                }
            )

        except Exception as e:
            # This is a catch all exception, edit this part to fit your needs.
            print("Something Happened: ", e)
            return e
    

        # after upload file to s3 bucket, return filename of the uploaded file
        return image.filename
    