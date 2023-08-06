mutation = '''
    mutation {
        tokenAuth(username: "%s", password: "%s") {
            token
        }
    }
'''

def token_auth_mutation(username, password):
    return mutation % (username, password)
