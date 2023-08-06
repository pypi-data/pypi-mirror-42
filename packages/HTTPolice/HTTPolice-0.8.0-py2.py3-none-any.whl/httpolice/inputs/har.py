# -*- coding: utf-8; -*-

import base64
import io
import json
import re
from urllib.parse import urlparse

from httpolice import framing1
from httpolice.exchange import Exchange
from httpolice.helpers import pop_pseudo_headers
from httpolice.inputs.common import InputError
from httpolice.known import h, m, media, st
from httpolice.parse import ParseError
from httpolice.request import Request
from httpolice.response import Response
from httpolice.stream import Stream
from httpolice.structure import (FieldName, StatusCode, Unavailable, http2,
                                 http11)
from httpolice.util.text import decode_path


def har_input(paths):
    for path in paths:
        # According to the spec, HAR files are UTF-8 with an optional BOM.
        path = decode_path(path)
        with io.open(path, 'rt', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
            except ValueError as exc:
                raise InputError('%s: bad HAR file: %s' % (path, exc)) from exc
            try:
                creator = CreatorInfo(data['log']['creator'])
                for entry in data['log']['entries']:
                    yield _process_entry(entry, creator, path)
            except (TypeError, KeyError) as exc:
                raise InputError('%s: cannot understand HAR file: %r' %
                                 (path, exc)) from exc


def _process_entry(data, creator, path):
    req = _process_request(data['request'], creator, path)
    resp = _process_response(data['response'], req, creator, path)
    return Exchange(req, [resp] if resp is not None else [])


def _process_request(data, creator, path):
    (version, header_entries, pseudo_headers) = _process_message(data, creator)
    if creator.is_chrome and version == http11 and u':host' in pseudo_headers:
        # SPDY exported from Chrome.
        version = None

    # Firefox exports "Connection: keep-alive" on HTTP/2 requests
    # (which triggers notice 1244)
    # even though it does not actually send it
    # (this can be verified with SSLKEYLOGFILE + Wireshark).
    if creator.is_firefox and version == http2:
        header_entries = [
            (name, value)
            for (name, value) in header_entries
            if (name, value) != (h.connection, u'keep-alive')
        ]

    method = data['method']
    header_names = {name for (name, _) in header_entries}

    parsed = urlparse(data['url'])
    scheme = parsed.scheme

    if creator.is_insomnia:
        # https://github.com/getinsomnia/insomnia/issues/840
        if h.host not in header_names:
            header_entries.insert(0, (h.host, parsed.netloc))
        if h.user_agent not in header_names:
            # The actual version can probably be extracted from
            ua_string = u'insomnia/%s' % creator.reconstruct_insomnia_version()
            header_entries.append((h.user_agent, ua_string))
        if h.accept not in header_names:
            header_entries.append((h.accept, u'*/*'))
        header_names = {name for (name, _) in header_entries}

    if method == m.CONNECT:
        target = parsed.netloc
    elif h.host in header_names:
        # With HAR, we can't tell if the request was to a proxy or to a server.
        # So we force most requests into the "origin form" of the target,
        target = parsed.path
        if parsed.query:
            target += u'?' + parsed.query
    else:
        # However, if the request has no ``Host`` header,
        # the user won't be able to see the target host
        # unless we set the full URL ("absolute form") as the target.
        # To prevent this from having an effect on the proxy logic,
        # we explicitly set `Request.is_to_proxy` to `None` later.
        target = data['url']

    if data['bodySize'] == 0:
        # No body, or a body of length 0 (which we do not distinguish).
        body = b''
    elif data['bodySize'] > 0:
        # A message body was present, but we cannot recover it,
        # because message body is the body *with* ``Content-Encoding``,
        # and HAR does not include that.
        body = Unavailable()
    else:
        # Unknown. Maybe there was a body, maybe there wasn't.
        body = None

    text = None
    post = data.get('postData')
    if post and post.get('text'):
        text = post['text']

        if creator.is_firefox and \
                post['mimeType'] == media.application_x_www_form_urlencoded \
                and u'\r\n' in text:
            # Yes, Firefox actually outputs this stuff. Go figure.
            (wtf, actual_text) = text.rsplit(u'\r\n', 1)
            try:
                buf = io.BufferedReader(io.BytesIO(wtf.encode('iso-8859-1')))
                more_entries = framing1.parse_header_fields(Stream(buf))
            except (UnicodeError, ParseError):      # pragma: no cover
                pass
            else:
                header_entries.extend(more_entries)
                text = actual_text

        if creator.is_fiddler and method == m.CONNECT and u'Fiddler' in text:
            # Fiddler's HAR export adds a body with debug information
            # to CONNECT requests.
            text = None
            body = b''

    req = Request(scheme, method, target, version, header_entries, body,
                  remark=u'from %s' % path)
    if text is not None:
        req.unicode_body = text
    req.is_to_proxy = None                      # See above.
    return req


def _process_response(data, req, creator, path):
    if data['status'] == 0:          # Indicates error in Chrome.
        return None
    (version, header_entries, _) = _process_message(data, creator)
    status = StatusCode(data['status'])
    reason = data['statusText']

    if creator.is_firefox:
        # Firefox joins all ``Set-Cookie`` response fields with newlines.
        # (It also joins other fields with commas,
        # but that is permitted by RFC 7230 Section 3.2.2.)
        header_entries = [
            (name, value)
            for (name, joined_value) in header_entries
            for value in (joined_value.split(u'\n') if name == h.set_cookie
                          else [joined_value])
        ]

    if creator.is_fiddler and req.method == m.CONNECT and status.successful:
        # Fiddler's HAR export adds extra debug headers to CONNECT responses
        # after the tunnel is closed.
        header_entries = [(name, value)
                          for (name, value) in header_entries
                          if name not in [u'EndTime', u'ClientToServerBytes',
                                          u'ServerToClientBytes']]

    # The logic for body is similar to that for requests (see above),
    # except that
    # (1) Firefox also includes a body with 304 responses;
    # (2) browsers may set ``bodySize = -1`` even when ``content.size >= 0``.
    if data['bodySize'] == 0 or data['content']['size'] == 0 or \
            status == st.not_modified:
        body = b''
    elif data['bodySize'] > 0 or data['content']['size'] > 0:
        body = Unavailable()
    else:
        body = None

    if version == http11 and creator.is_firefox and \
            any(name == u'x-firefox-spdy' for (name, _) in header_entries):
        # Helps with SPDY in Firefox.
        version = None
    if creator.is_chrome and version != req.version:
        # Helps with SPDY in Chrome.
        version = None

    resp = Response(version, status, reason, header_entries, body=body,
                    remark=u'from %s' % path)

    if data['content'].get('text') and status != st.not_modified:
        if data['content'].get('encoding', u'').lower() == u'base64':
            try:
                decoded_body = base64.b64decode(data['content']['text'])
            except ValueError:
                # Firefox sometimes marks normal, unencoded text as "base64"
                # (see ``test/har_data/firefox_gif.har``).
                # But let's not try to guess.
                pass
            else:
                if creator.is_fiddler and req.method == m.CONNECT and \
                        status.successful and b'Fiddler' in decoded_body:
                    # Fiddler's HAR export adds a body with debug information
                    # to CONNECT responses.
                    resp.body = b''
                else:
                    resp.decoded_body = decoded_body

        elif 'encoding' not in data['content']:
            resp.unicode_body = data['content']['text']

    return resp


def _process_message(data, creator):
    header_entries = [(FieldName(d['name']), d['value'])
                      for d in data['headers']]
    pseudo_headers = pop_pseudo_headers(header_entries)
    if creator.is_edge:         # Edge exports HTTP/2 messages as HTTP/1.1.
        version = None
    elif creator.is_insomnia:   # Insomnia's HAR export hardcodes HTTP/1.1.
        version = None
    elif data['httpVersion'] == u'unknown':           # Used by Chrome.
        version = None
    else:
        version = data['httpVersion'].upper()
        if version == u'HTTP/2.0':          # Used by Firefox, Chrome, ...
            version = http2
    return (version, header_entries, pseudo_headers)


class CreatorInfo(dict):

    __slots__ = []

    @property
    def is_chrome(self):
        return self['name'] == u'WebInspector'

    @property
    def is_firefox(self):
        # Not sure if "Iceweasel" is actually used, but it won't hurt.
        return self['name'] in [u'Firefox', u'Iceweasel']

    @property
    def is_edge(self):
        return self['name'] == u'F12 Developer Tools'

    @property
    def is_fiddler(self):
        return self['name'] == u'Fiddler'

    @property
    def is_insomnia(self):
        return self['name'] == u'Insomnia REST Client'

    def reconstruct_insomnia_version(self):
        match = re.search(r'v([0-9]+\.[0-9]+\.[0-9]+)', self['version'])
        if not match:               # pragma: no cover
            return u'x.x.x'
        return match.groups(1)
