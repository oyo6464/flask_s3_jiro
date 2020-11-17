import boto3



#uploadする関数
def upload_file(file_name, bucket):
    #保存する名前を決める
    object_name = file_name
    s3_client = boto3.client("s3")

    
    response = s3_client.upload_file(file_name,bucket,object_name)

    return response



#画像をDLする関数
def download_file(file_name,bucket):
    s3 = boto3.resource("s3")
    #output = f"downloads/{file_name}"

    #{{meta.id}}{{meta.p_filename}}
    s3.Bucket(bucket).download_file(file_name, file_name)
    return file_name



#jsonをDLする関数
def download_json(bucket):
    s3 = boto3.resource("s3")
    output = "data/data.json"
    s3.Bucket(bucket).download_file(output, output)
    return output




#S3バケット内のファイルを取得し、名前の一覧表示をする
def list_files(bucket):
    s3 = boto3.client("s3")
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents
