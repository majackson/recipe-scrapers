from urlparse import urlparse, ParseResult

def rel_to_abs(start_path, relative_url):
    """converts a relative url at a specified (absolute) location
    params:
    start_path - the absolute path from which the relative 
    url is being accessed
    relative_url - the relative url on the page"""
    remove_null = lambda x: bool(x)
    parsed_start_url = urlparse(start_path)
    path_items = remove_null(parsed_start_url.path.split('/') + [relative_url]) 
    new_path = '/'.join(path_items)
    parsed_abs_url = ParseResult(
                        scheme=parsed_start_url.scheme,
                        netloc=parsed_start_url.netloc,
                        path=new_path,
                        params=parsed_start_url.params,
                        query=parsed_start_url.query,
                        fragment=parsed_start_url.fragment)
    return parsed_abs_url.geturl()

