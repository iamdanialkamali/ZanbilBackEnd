import jwt

TOKEN_KEY = 'p3b_f2flrj^97^a#=3%o&6k&59pb7u%f^29djo9$6m-*9i5d*a'

class Tokenizer:

    def endcode(self,message):
        encoded = jwt.encode(message, TOKEN_KEY, algorithm='HS256')

        return encoded

    def decode(self,token):
        return  jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])

    def user_token_generator(self,user):
        message = {
            'id': user.id
        }
        encoded = jwt.encode(message, TOKEN_KEY, algorithm='HS256')
        return { "jwt" :encoded}
    def meta_encode(self,meta):
        token = meta.split(' ')[1]
        message = jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])
        return message['id']