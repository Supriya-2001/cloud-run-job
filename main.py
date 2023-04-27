from tempfile import NamedTemporaryFile
import pandas as pd
from google.cloud import storage
import os
# import json
# from flask import Flask, request

# app = Flask(__name__)


# @app.route('/', methods=['POST'])
def convert_csv_to_parquet():
    # content_type = request.headers.get('Content-Type')
    # if(content_type=='application/json'):
    #     gcs_json = json.loads(request.data)
    # else:
    #     return "Checking for JSON failed"

    # file_path = gcs_json['file_path']
    # file_name = gcs_json['file_name']
    # bucket_name = gcs_json['bucket_name']
    file_path= 'gs://csvfile-bucket/csv (1).csv'
   

    i=0
    chunk_count = 0
    converted_bucket_name = "parquetfile-bucket"
    CHUNK_SIZE = 100000  # 1GB
    
    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
        modification_of_csv_file(chunk)
        print("Modification is done")

        converted_blob_name = 'Data{}'.format(i) + '.parquet'
        parquet_file_path = 'gs://{}/{}'.format(converted_bucket_name,converted_blob_name)

        chunk.to_parquet(parquet_file_path, engine="fastparquet", compression="snappy")
    
        print(f"{chunk.shape} of csv data is converted to parquet")

        
        print("chunk is uploaded to bucket")

       

        chunk_count += 1
        i += 1   

    print("All files are uploaded to gcs bucket")


    print("Trying to create a new file")
    Compose_all_file(chunk_count)
    delete_parquet_files(chunk_count)

    return "Success"

def Compose_all_file(chunk_count):
    storage_client = storage.Client()
    converted_bucket_name = "parquetfile-bucket"
    bucket = storage_client.bucket(converted_bucket_name)
    destination = bucket.blob('Final.parquet')
    mylist = []
    for j in range(chunk_count):
        mylist.append(bucket.blob('Data{}'.format(j) + '.parquet'))
        j +=1


    destination.compose(mylist)
    


def delete_parquet_files(chunk_count):
    storage_client = storage.Client()
    converted_bucket_name = "parquetfile-bucket"
    bucket = storage_client.bucket(converted_bucket_name)
    for i in range(chunk_count):
        destination = bucket.blob('Data{}'.format(i) + '.parquet')
        destination.delete()

    
def modification_of_csv_file(chunk):
    chunk['Full Name'] = chunk['First Name'] + ' ' + chunk['Last Name']
    chunk['Total Marks'] = chunk['Maths'] + chunk['Science'] + chunk['English']+ chunk['History']


if __name__ == "__main__":
    convert_csv_to_parquet()
    # port= int(os.environ.get('PORT',8080))
    # app.run(debug=True,host='0.0.0.0',port=port)

