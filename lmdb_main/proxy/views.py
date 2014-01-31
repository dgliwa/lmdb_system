from django.http import HttpResponse
import mimetypes
import urllib2


def proxy_to(request, path):
	if request.META.has_key('QUERY_STRING'):
		url = request.META['QUERY_STRING']
	try:
		proxied_request = urllib2.urlopen(url)
		status_code = proxied_request.code
		mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
		content = proxied_request.read()
	except urllib2.HTTPError as e:
		return HttpResponse(e.msg, status=e.code, mimetype='text/plain')
	else:
		return HttpResponse(content, status=status_code, mimetype=mimetype)