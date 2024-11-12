import boto3
import io
from flask import Flask,render_template,request
from PIL import Image

app = Flask(__name__)

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image_path']
        image = Image.open(image_file)
        stream = io.BytesIO()
        image.save(stream, format="JPEG")
        image_binary = stream.getvalue()

    response = rekognition.search_faces_by_image(
        CollectionId='family_collection2',
        Image={'Bytes':image_binary}                                       
        )
    
    for match in response['FaceMatches']:
        print (match['Face']['FaceId'],match['Face']['Confidence'])
        
    face = dynamodb.get_item(
        TableName='family_collection2',  
        Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )
    recognized_faces = [

    ]
    if 'Item' in face:
        return render_template('result.html', recognized_faces=recognized_faces)
    else:
        return render_template('result.html', error="Pessoa não reconhecida")
    return render_template('index.html')
