import os

from qiniu import Auth, put_file, etag

qiniu_ak = os.environ.get('QINIU_ACCESS_KEY')
qiniu_sk = os.environ.get('QINIU_SECRET_KEY')
bucket_name = os.environ.get('QINIU_BUCKET_NAME', 'nmsltongjidbproject')

q = Auth(qiniu_ak, qiniu_sk)


def upload(file_name: str, local_file_path: str):
    # 生成上传 Token，可以指定过期时间等
    policy = {
        "mimeLimit": "image/*",
    }
    token = q.upload_token(bucket_name, file_name, 3600, policy=policy)
    # 要上传文件的本地路径
    ret, info = put_file(token, file_name, local_file_path)
    # print(ret, '\n\n', info)
    return ret, info
