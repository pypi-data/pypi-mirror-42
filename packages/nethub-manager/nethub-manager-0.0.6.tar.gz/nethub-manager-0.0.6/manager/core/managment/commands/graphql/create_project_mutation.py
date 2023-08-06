mutation = '''
    mutation {
        createProject(input: {
            title:"%s",
            library:"%s"
        }) {
            project {
                gitAddress
            }
        }
    }
'''

def create_project_mutation(name, lib_name):
    return mutation % (name, lib_name)
