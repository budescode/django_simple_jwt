
def custom_error_msg(error):
    try:
        keys = error.keys() #get the keys in the error object
        keys_list = list(keys) #turn the keys to list
        err_str = '' # default error msg is an empty string
        for i in keys_list: #loop through the eror list
            theerror = error[i]  #get the data of an object which is another list
            for e in theerror:
                finalerr = f'{i}: {e}'
                err_str = err_str + f'{finalerr} '
        return err_str
    except:        
        return str(error)

# def response_msg(message, data, status):
#     return Response