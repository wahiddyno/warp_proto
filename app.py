from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import boto3
from itsdangerous import URLSafeSerializer
from config import S3_BUCKET, S3_KEY, S3_SECRET, INDEX, link_prefix
from flask import session


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'warpit'
auth_s = URLSafeSerializer(app.secret_key, "auth")


def _get_s3_resource():
    if S3_KEY and S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.resource('s3')


def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        bucket = S3_BUCKET

    return s3_resource.Bucket(bucket)


def get_buckets_list():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')


def put_object(obj):
    file_name = obj.filename
    token = auth_s.dumps(file_name)
    bucket_obj = get_bucket()
    bucket_obj.Object(token).put(Body=obj)
    return(token)


@app.route('/')
def index():
    global link_prefix
    link_prefix == request.base_url
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    current_file = request.files['file']
    key = put_object(obj=current_file)
    return render_template('successful.html', key=link_prefix + str(key))


@app.route('/download/<token>')
def download(token):
    assert token == request.view_args['token']
    bucket_obj = get_bucket()
    file_obj = bucket_obj.Object(token).get()
    file_name = auth_s.loads(token)
    return Response(
        file_obj['Body'].read(),
        mimetype='application/octet-stream',
        headers={
            "Content-Disposition": "attachment;filename={}".format(file_name)}
    )


if __name__ == "__main__":
    app.run()
