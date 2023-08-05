# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Chris Caron <lead2gold@gmail.com>
# All rights reserved.
#
# This code is licensed under the MIT License.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from apprise.plugins.NotifyBase import NotifyBase
from apprise import NotifyType
from apprise import NotifyImageSize
from timeit import default_timer
from apprise.utils import compat_is_basestring


def test_notify_base():
    """
    API: NotifyBase() object

    """

    # invalid types throw exceptions
    try:
        nb = NotifyBase(**{'format': 'invalid'})
        # We should never reach here as an exception should be thrown
        assert(False)

    except TypeError:
        assert(True)

    # Bad port information
    nb = NotifyBase(port='invalid')
    assert nb.port is None

    nb = NotifyBase(port=10)
    assert nb.port == 10

    # Throttle overrides..
    nb = NotifyBase()
    nb.throttle_attempt = 0.0
    start_time = default_timer()
    nb.throttle()
    elapsed = default_timer() - start_time
    # Should be a very fast response time since we set it to zero but we'll
    # check for less then 500 to be fair as some testing systems may be slower
    # then other
    assert elapsed < 0.5

    start_time = default_timer()
    nb.throttle(1.0)
    elapsed = default_timer() - start_time
    # Should be a very fast response time since we set it to zero but we'll
    # check for less then 500 to be fair as some testing systems may be slower
    # then other
    assert elapsed < 1.5

    # our NotifyBase wasn't initialized with an ImageSize so this will fail
    assert nb.image_url(notify_type=NotifyType.INFO) is None
    assert nb.image_path(notify_type=NotifyType.INFO) is None
    assert nb.image_raw(notify_type=NotifyType.INFO) is None

    # Color handling
    assert nb.color(notify_type='invalid') is None
    assert compat_is_basestring(
        nb.color(notify_type=NotifyType.INFO, color_type=None))
    assert isinstance(
        nb.color(notify_type=NotifyType.INFO, color_type=int), int)
    assert isinstance(
        nb.color(notify_type=NotifyType.INFO, color_type=tuple), tuple)

    # Create an object
    nb = NotifyBase()
    # Force an image size since the default doesn't have one
    nb.image_size = NotifyImageSize.XY_256

    # We'll get an object this time around
    assert nb.image_url(notify_type=NotifyType.INFO) is not None
    assert nb.image_path(notify_type=NotifyType.INFO) is not None
    assert nb.image_raw(notify_type=NotifyType.INFO) is not None

    # But we will not get a response with an invalid notification type
    assert nb.image_url(notify_type='invalid') is None
    assert nb.image_path(notify_type='invalid') is None
    assert nb.image_raw(notify_type='invalid') is None

    # Static function testing
    assert NotifyBase.escape_html("<content>'\t \n</content>") == \
        '&lt;content&gt;&apos;&emsp;&nbsp;\n&lt;/content&gt;'

    assert NotifyBase.escape_html(
        "<content>'\t \n</content>", convert_new_lines=True) == \
        '&lt;content&gt;&apos;&emsp;&nbsp;&lt;br/&gt;&lt;/content&gt;'

    assert NotifyBase.split_path(
        '/path/?name=Dr%20Disrespect', unquote=False) == \
        ['path', '?name=Dr%20Disrespect']

    assert NotifyBase.split_path(
        '/path/?name=Dr%20Disrespect', unquote=True) == \
        ['path', '?name=Dr', 'Disrespect']

    # Test is_email
    assert NotifyBase.is_email('test@gmail.com') is True
    assert NotifyBase.is_email('invalid.com') is False

    # Test is_hostname
    assert NotifyBase.is_hostname('example.com') is True

    # Test quote
    assert NotifyBase.unquote('%20') == ' '
    assert NotifyBase.quote(' ') == '%20'
    assert NotifyBase.unquote(None) == ''
    assert NotifyBase.quote(None) == ''


def test_notify_base_urls():
    """
    API: NotifyBase() URLs

    """

    # Test verify switch whih is used as part of the SSL Verification
    # by default all SSL sites are verified unless this flag is set to
    # something like 'No', 'False', 'Disabled', etc.  Boolean values are
    # pretty forgiving.
    results = NotifyBase.parse_url('https://localhost:8080/?verify=No')
    assert 'verify' in results
    assert results['verify'] is False

    results = NotifyBase.parse_url('https://localhost:8080/?verify=Yes')
    assert 'verify' in results
    assert results['verify'] is True

    # The default is to verify
    results = NotifyBase.parse_url('https://localhost:8080')
    assert 'verify' in results
    assert results['verify'] is True

    # Password Handling

    # pass keyword over-rides default password
    results = NotifyBase.parse_url('https://user:pass@localhost')
    assert 'password' in results
    assert results['password'] == "pass"

    # pass keyword over-rides default password
    results = NotifyBase.parse_url(
        'https://user:pass@localhost?pass=newpassword')
    assert 'password' in results
    assert results['password'] == "newpassword"

    # pass headers
    results = NotifyBase.parse_url(
        'https://localhost:8080?-HeaderKey=HeaderValue')
    assert 'headerkey' in results['headers']
    assert results['headers']['headerkey'] == 'HeaderValue'

    # User Handling

    # user keyword over-rides default password
    results = NotifyBase.parse_url('https://user:pass@localhost')
    assert 'user' in results
    assert results['user'] == "user"

    # user keyword over-rides default password
    results = NotifyBase.parse_url(
        'https://user:pass@localhost?user=newuser')
    assert 'user' in results
    assert results['user'] == "newuser"

    # Test invalid urls
    assert NotifyBase.parse_url('https://:@/') is None
    assert NotifyBase.parse_url('http://:@') is None
    assert NotifyBase.parse_url('http://@') is None
    assert NotifyBase.parse_url('http:///') is None
    assert NotifyBase.parse_url('http://:test/') is None
    assert NotifyBase.parse_url('http://pass:test/') is None
