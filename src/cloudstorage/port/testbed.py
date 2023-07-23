from cloudstorage import common as gcs_common
from cloudstorage.port import stub_dispatcher as gcs_dispatcher


def urlfetch_to_gcs_stub(url, payload, method, headers, request, response,
                         follow_redirects=False, deadline=None,
                         validate_certificate=None, http_proxy=None):

  """Forwards Google Cloud Storage `urlfetch` requests to gcs_dispatcher."""
  headers_map = dict(
      (header.key().lower(), header.value()) for header in headers)
  result = gcs_dispatcher.dispatch(method, headers_map, url, payload)
  response.set_statuscode(result.status_code)
  response.set_content(result.content[:urlfetch_stub.MAX_RESPONSE_SIZE])
  for k, v in result.headers.iteritems():
    if k.lower() == 'content-length' and method != 'HEAD':
      v = len(response.content())
    header_proto = response.add_header()
    header_proto.set_key(k)
    header_proto.set_value(str(v))
  if len(result.content) > urlfetch_stub.MAX_RESPONSE_SIZE:
    response.set_contentwastruncated(True)


def urlmatcher_for_gcs_stub(url):
  """Determines whether a URL should be handled by the Cloud Storage stub."""
  return url.startswith(gcs_common.local_api_url())



GCS_URLMATCHERS_TO_FETCH_FUNCTIONS = [
    (urlmatcher_for_gcs_stub, urlfetch_to_gcs_stub)]
