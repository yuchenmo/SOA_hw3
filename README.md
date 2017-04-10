# SOA_hw3

SOA homework 3

## Intentions

-	Login with face
-	Natural language understanding
-	Cloud user-defined ML service

## Structure

-	Face API: Wrapped Microsoft Cognitive Service APIs
-	Login API: Wrapped Face API for back-end usage
-	LUIS API: Wrapped Microsoft LUIS SDK
-	Price Pridicting model: Wrapped Microsoft Machine Learning Framework

## LoginAPI Example

-	Initialize

		from loginapi import LoginAPI
		env = LoginAPI()

-	Add person

		env.create_person('name')
		
-	Add face for someone

		env.add_face('name', 'xxx.jpg')

-	Try login with an image

		env.login_with_face('xxx.jpg')
		
-	apikey.json includes 'key', 'ml_api_key', 'workspace_id', 'service_id', 'LUIS_app_id', 'LUIS_appkey' provided by corresponding Microsoft service website.


## Acknowlegdement

-	Webcam.js
-	Microsoft LUIS SDK