# SOA_hw3

SOA homework 3


## Structure

-	Face API: Wrapped Microsoft Cognitive Service APIs
-	Login API: Wrapped Face API for back-end usage

## Example

-	Initialize

		from loginapi import LoginAPI
		env = LoginAPI()

-	Add person

		env.create_person('name')
		
-	Add face for someone

		env.add_face('name', 'xxx.jpg')

-	Try login with an image

		env.login_with_face('xxx.jpg')


## Acknowlegdement

-	[jpegcam](https://code.google.com/archive/p/jpegcam/downloads). Rearranged files to suit Django style