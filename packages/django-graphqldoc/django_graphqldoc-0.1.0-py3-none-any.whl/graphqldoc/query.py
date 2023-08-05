general_query = '''
query {
  __schema {
    types {
      name
      description
      kind
    }
    queryType{
      name
      fields {
        name
        description
				args {
          name
				  description
          type {
            name
            kind
          }
				}
        type {
          name
          kind
          description
        }
      }
    }
    mutationType{
      name
      fields {
        name
        description
				args {
          name
				  description
          type {
            name
            ofType {
              name
              kind
            }
          }
				}
        type {
          name
          kind
          description
        }
      }
    }
  }
}
'''

schema_query = '''
query {
  __schema {
    types {
      name
      description
      kind
    }
  }
}
'''

type_query = '''
query t {
  __type(name: "@TYPE_NAME") {
    kind
    name
    description
    fields {
      name
      description
      type {
        kind
        name
        description
      }
      args {
        name
        description
        type {
          kind
          name
          fields {
            name
          }
          ofType {
            name
          }
        }
      }
    }
    inputFields {
      name
      description
      type {
        name
        kind
      }
    }
    interfaces {
      name
      description
    }
    possibleTypes {
      name
      description
    }
    enumValues {
      name
      description
    }
  }
}
'''

def get_query(_type, name=None):
    if _type == 'schema':
        return schema_query
    if _type == 'general':
        return general_query
    if _type == 'type':
        return type_query.replace('@TYPE_NAME', name)