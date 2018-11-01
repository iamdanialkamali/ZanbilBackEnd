import jwt

TOKEN_KEY = 'p3b_f2flrj^97^a#=3%o&6k&59pb7u%f^29djo9$6m-*9i5d*a'

class Tokenizer:

    @staticmethod
    def endcode(message):
        encoded = jwt.encode(message, TOKEN_KEY, algorithm='HS256')

        return encoded

    @staticmethod
    def decode(token):
        return  jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])

    @staticmethod
    def user_token_generator(user):
        message = {
            'id': user.id
        }
        encoded = jwt.encode(message, TOKEN_KEY, algorithm='HS256')
        return { "jwt" :encoded}

    @staticmethod
    def meta_encode(meta):

        token = meta['HTTP_AUTHORIZATION'].split(' ')[1]
        message = jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])

        return message['id']
