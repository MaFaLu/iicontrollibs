def application(environ, start_response):
 
    import cgi
    import json
    
    import os,sys,inspect

    # Set top folder to allow import of modules

    top_folder = os.path.split(os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))[0]
    if top_folder not in sys.path:
        sys.path.insert(0,top_folder)

    from iiutilities.datalib import gettimestring
    from iiutilities.dblib import sqlitequery

    # post_env = environ.copy()
    # post_env['QUERY_STRING'] = ''
    # post = cgi.FieldStorage(
    #     fp=environ['wsgi.input'],
    #     environ=post_env,
    #     keep_blank_values=True
    # )
    #
    # formname=post.getvalue('name')
    #
    # post={}
    # for k in post.keys():
    #     post[k] = post.getvalue(k)

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    post = json.loads(request_body.decode('utf-8'))

    output = {}
    output['message'] = ''

    status = '200 OK'

    if 'sessionid' in post.keys() and 'event' in post.keys() and 'realIP' in post.keys() and 'apparentIP' in post.keys():
        # sessionid contains the session id
        sessionid = post.getvalue('sessionid')
        if post.getvalue('event') == 'access':
            accesstime = gettimestring()
            username = post.getvalue('username')
            apparentIP = post.getvalue('apparentIP')
            realIP =  post.getvalue('realIP')
            sqlitequery('/var/www/data/authlog.db',"insert into sessionlog values ( \'" + username + "\',\'" + sessionid + "\',\'" + accesstime + "\'," + "\'access\' ,\'" + apparentIP + "\',\'" + realIP + "\' )")
        output = "Output processed for " + realIP + " & " + apparentIP

    else:
        output = 'error: no session field sent'  

    response_headers = [('Content-type', 'text/plain'), ('Content-Length',str(len(output)))]
    start_response(status,response_headers)
   
    return [output]


    

