import hashlib

def hash_password(s:str)->str:
    return md5(s + '普通上班组')

def md5(s:str)->str:
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()

def apply_query_filter(query_filter:dict,target_class,target_query):
    for k in query_filter:
        if type(query_filter[k])==list:
            query_filter[k] = query_filter[k][0]
    query_dict = {}
    for k in query_filter:
        if query_filter[k]!='' and hasattr(target_class,k):
            query_dict[k]=query_filter[k]
            print('+"{}:{}'.format(k,query_filter[k]))
    for k in query_dict:
        target_query = target_query.filter(getattr(target_class,k).like('%%'+query_dict[k]+'%%'))
    return target_query

if __name__ == "__main__":
    print(md5('hello'))
