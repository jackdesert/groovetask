from pprint import pformat

def application(environ, start_response):
    # show the environment:
    output = ['<pre>']
    output.append(pformat(environ))
    output.append('</pre>')

    #create a simple form:
    output.append('<form method="post">')
    output.append('<input type="text" name="test">')
    output.append('<input type="submit">')
    output.append('</form>')

    if environ['REQUEST_METHOD'] == 'POST':
        # show form data as received by POST:
        output.append('<h1>FORM DATA</h1>')
        output.append(pformat(environ['wsgi.input'].read()))

    # send results
    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])
    return output
