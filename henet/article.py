from datetime import datetime

class Article(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        if 'metadata' not in self:
            self['metadata'] = {}
            self['metadata_source'] = ''
        if 'title_source' not in self:
            self['title_source'] = ''
        if 'body' not in self:
            self['body'] = ''

    def set_metadata(self, key, value):
        self['metadata'][key.lower()] = value
        self._update_metadata_source()

    def _update_metadata_source(self):
        def _convert(value):
            if isinstance(value, datetime):
                return unicode(value.strftime('%Y-%m-%d %H:%M'))
            if isinstance(value, str):
                return value.decode('utf8')
            return value

        metadata = [u':%s: %s' % (name, _convert(value)) for name, value in
                    self['metadata'].items()]
        metadata = u'\n'.join(metadata)
        self['metadata_source'] = metadata

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        if key == 'title':
            self['title_source'] = val + u'\n' + u'=' * len(val)

    def render(self):
        res = self['title_source'] + u'\n\n'
        res += self['metadata_source'] + u'\n\n'
        res += self['body']
        if not res.endswith(u'\n'):
            res += u'\n'
        return res
