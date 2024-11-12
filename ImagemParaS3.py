import boto3

s3 = boto3.resource('s3')

images=[('1.jpeg','Sky'),
      ('2.jpeg','Lorenzo'),
      ('3.jpeg','Zico'),
      ('4.jpeg','Ana Clara'),
      ('5.jpeg','Rafael'),
      ('6.jpeg','Rafael Augusto'),
      ]  
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('facecollectionbucket10','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]}
                    )
