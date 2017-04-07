from loginapi import LoginAPI
from IPython import embed

env = LoginAPI()

# μ'sic forever
env.create_person('uchida_aya')
env.add_face('uchida_aya', 'http://img1.ak.crunchyroll.com/i/spire3/7a5a5be3fc79e1df30d2644a56ba30cb1452619985_full.jpg')
env.add_face('uchida_aya', 'https://pilefectionmedia.files.wordpress.com/2015/07/003.jpg?w=350&h=200&crop=1')

env.create_person('suzuko_mimori')
env.add_face('suzuko_mimori', 'https://s-media-cache-ak0.pinimg.com/736x/bf/8b/42/bf8b424a9473c78faf1459bd98732cd6.jpg')
env.add_face('suzuko_mimori', 'http://i1.jpopasia.com/assets/1/29728-suzukomimori-b0t4.jpg')

print (env.login_with_face('https://myanimelist.cdn-dena.com/images/voiceactors/3/24319.jpg'))
