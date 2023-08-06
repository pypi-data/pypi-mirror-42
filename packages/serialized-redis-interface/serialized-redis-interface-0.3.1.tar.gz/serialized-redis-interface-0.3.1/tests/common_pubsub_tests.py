import time

import pytest
import redis

from .conftest import skip_if_server_version_lt


def wait_for_message(pubsub, timeout=0.1, ignore_subscribe_messages=False):
    now = time.time()
    timeout = now + timeout
    while now < timeout:
        message = pubsub.get_message(
            ignore_subscribe_messages=ignore_subscribe_messages)
        if message is not None:
            return message
        time.sleep(0.01)
        now = time.time()
    return None


def make_message(type, channel, data, pattern=None):
    return {
        'type': type,
        'pattern': pattern or None,
        'channel': channel,
        'data': data
    }


def make_subscribe_test_data(pubsub, type):
    if type == 'channel':
        return {
            'p': pubsub,
            'sub_type': 'subscribe',
            'unsub_type': 'unsubscribe',
            'sub_func': pubsub.subscribe,
            'unsub_func': pubsub.unsubscribe,
            'keys': ['foo', 'bar', 'uni' + chr(4456) + 'code']
        }
    elif type == 'pattern':
        return {
            'p': pubsub,
            'sub_type': 'psubscribe',
            'unsub_type': 'punsubscribe',
            'sub_func': pubsub.psubscribe,
            'unsub_func': pubsub.punsubscribe,
            'keys': ['f*', 'b*', 'uni' + chr(4456) + '*']
        }
    assert False, 'invalid subscribe type: %s' % type


class TestPubSubSubscribeUnsubscribe(object):

    def _test_subscribe_unsubscribe(self, p, sub_type, unsub_type, sub_func,
                                    unsub_func, keys):
        for key in keys:
            assert sub_func(key) is None

        # should be a message for each channel/pattern we just subscribed to
        for i, key in enumerate(keys):
            assert wait_for_message(p) == make_message(sub_type, key, i + 1)

        for key in keys:
            assert unsub_func(key) is None

        # should be a message for each channel/pattern we just unsubscribed
        # from
        for i, key in enumerate(keys):
            i = len(keys) - 1 - i
            assert wait_for_message(p) == make_message(unsub_type, key, i)

    def test_channel_subscribe_unsubscribe(self, r):
        kwargs = make_subscribe_test_data(r.pubsub(), 'channel')
        self._test_subscribe_unsubscribe(**kwargs)

    def test_pattern_subscribe_unsubscribe(self, r):
        kwargs = make_subscribe_test_data(r.pubsub(), 'pattern')
        self._test_subscribe_unsubscribe(**kwargs)

    def _test_resubscribe_on_reconnection(self, p, sub_type, unsub_type,
                                          sub_func, unsub_func, keys):

        for key in keys:
            assert sub_func(key) is None

        # should be a message for each channel/pattern we just subscribed to
        for i, key in enumerate(keys):
            assert wait_for_message(p) == make_message(sub_type, key, i + 1)

        # manually disconnect
        p.connection.disconnect()

        # calling get_message again reconnects and resubscribes
        # note, we may not re-subscribe to channels in exactly the same order
        # so we have to do some extra checks to make sure we got them all
        messages = []
        for i in range(len(keys)):
            messages.append(wait_for_message(p))

        unique_channels = set()
        assert len(messages) == len(keys)
        for i, message in enumerate(messages):
            assert message['type'] == sub_type
            assert message['data'] == i + 1
            assert isinstance(message['channel'], str)
            unique_channels.add(message['channel'])

        assert len(unique_channels) == len(keys)
        for channel in unique_channels:
            assert channel in keys

    def test_resubscribe_to_channels_on_reconnection(self, r):
        kwargs = make_subscribe_test_data(r.pubsub(), 'channel')
        self._test_resubscribe_on_reconnection(**kwargs)

    def test_resubscribe_to_patterns_on_reconnection(self, r):
        kwargs = make_subscribe_test_data(r.pubsub(), 'pattern')
        self._test_resubscribe_on_reconnection(**kwargs)

    def _test_subscribed_property(self, p, sub_type, unsub_type, sub_func,
                                  unsub_func, keys):

        assert p.subscribed is False
        sub_func(keys[0])
        # we're now subscribed even though we haven't processed the
        # reply from the server just yet
        assert p.subscribed is True
        assert wait_for_message(p) == make_message(sub_type, keys[0], 1)
        # we're still subscribed
        assert p.subscribed is True

        # unsubscribe from all channels
        unsub_func()
        # we're still technically subscribed until we process the
        # response messages from the server
        assert p.subscribed is True
        assert wait_for_message(p) == make_message(unsub_type, keys[0], 0)
        # now we're no longer subscribed as no more messages can be delivered
        # to any channels we were listening to
        assert p.subscribed is False

        # subscribing again flips the flag back
        sub_func(keys[0])
        assert p.subscribed is True
        assert wait_for_message(p) == make_message(sub_type, keys[0], 1)

        # unsubscribe again
        unsub_func()
        assert p.subscribed is True
        # subscribe to another channel before reading the unsubscribe response
        sub_func(keys[1])
        assert p.subscribed is True
        # read the unsubscribe for key1
        assert wait_for_message(p) == make_message(unsub_type, keys[0], 0)
        # we're still subscribed to key2, so subscribed should still be True
        assert p.subscribed is True
        # read the key2 subscribe message
        assert wait_for_message(p) == make_message(sub_type, keys[1], 1)
        unsub_func()
        # haven't read the message yet, so we're still subscribed
        assert p.subscribed is True
        assert wait_for_message(p) == make_message(unsub_type, keys[1], 0)
        # now we're finally unsubscribed
        assert p.subscribed is False

    def test_subscribe_property_with_channels(self, r):
        kwargs = make_subscribe_test_data(r.pubsub(), 'channel')
        self._test_subscribed_property(**kwargs)

    def test_subscribe_property_with_patterns(self, r):
        kwargs = make_subscribe_test_data(r.pubsub(), 'pattern')
        self._test_subscribed_property(**kwargs)

    def test_ignore_all_subscribe_messages(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)

        checks = (
            (p.subscribe, 'foo'),
            (p.unsubscribe, 'foo'),
            (p.psubscribe, 'f*'),
            (p.punsubscribe, 'f*'),
        )

        assert p.subscribed is False
        for func, channel in checks:
            assert func(channel) is None
            assert p.subscribed is True
            assert wait_for_message(p) is None
        assert p.subscribed is False

    def test_ignore_individual_subscribe_messages(self, r):
        p = r.pubsub()

        checks = (
            (p.subscribe, 'foo'),
            (p.unsubscribe, 'foo'),
            (p.psubscribe, 'f*'),
            (p.punsubscribe, 'f*'),
        )

        assert p.subscribed is False
        for func, channel in checks:
            assert func(channel) is None
            assert p.subscribed is True
            message = wait_for_message(p, ignore_subscribe_messages=True)
            assert message is None
        assert p.subscribed is False


class TestPubSubMessages(object):

    def setup_method(self, method):
        self.message = None

    def message_handler(self, message):
        self.message = message

    def test_published_message_to_channel(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        p.subscribe('foo')
        assert r.publish('foo', {'complex': ['test', 'message']}) == 1

        message = wait_for_message(p)
        assert isinstance(message, dict)
        assert message == make_message('message', 'foo', {'complex': ['test', 'message']})

    def test_published_message_to_pattern(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        p.subscribe('foo')
        p.psubscribe('f*')
        # 1 to pattern, 1 to channel
        assert r.publish('foo', {'complex': ['test', 'message']}) == 2

        message1 = wait_for_message(p)
        message2 = wait_for_message(p)
        assert isinstance(message1, dict)
        assert isinstance(message2, dict)

        expected = [
            make_message('message', 'foo', {'complex': ['test', 'message']}),
            make_message('pmessage', 'foo', {'complex': ['test', 'message']}, pattern='f*')
        ]

        assert message1 in expected
        assert message2 in expected
        assert message1 != message2

    def test_channel_message_handler(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        p.subscribe(foo=self.message_handler)
        assert r.publish('foo', {'complex': ['test', 'message']}) == 1
        assert wait_for_message(p) is None
        assert self.message == make_message('message', 'foo', {'complex': ['test', 'message']})

    def test_pattern_message_handler(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        p.psubscribe(**{'f*': self.message_handler})
        assert r.publish('foo', {'complex': ['test', 'message']}) == 1
        assert wait_for_message(p) is None
        assert self.message == make_message('pmessage', 'foo', {'complex': ['test', 'message']},
                                            pattern='f*')

    def test_unicode_channel_message_handler(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        channel = 'uni' + chr(4456) + 'code'
        channels = {channel: self.message_handler}
        p.subscribe(**channels)
        assert r.publish(channel, {'complex': ['test', 'message']}) == 1
        assert wait_for_message(p) is None
        assert self.message == make_message('message', channel, {'complex': ['test', 'message']})

    def test_unicode_pattern_message_handler(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        pattern = 'uni' + chr(4456) + '*'
        channel = 'uni' + chr(4456) + 'code'
        p.psubscribe(**{pattern: self.message_handler})
        assert r.publish(channel, {'complex': ['test', 'message']}) == 1
        assert wait_for_message(p) is None
        assert self.message == make_message('pmessage', channel,
                    {'complex': ['test', 'message']}, pattern=pattern)

    def test_get_message_without_subscribe(self, r):
        p = r.pubsub()
        with pytest.raises(RuntimeError) as info:
            p.get_message()
        expect = ('connection not set: '
                  'did you forget to call subscribe() or psubscribe()?')
        assert expect in info.exconly()


class TestPubSubRedisDown(object):

    def test_channel_subscribe(self, r):
        r = redis.Redis(host='localhost', port=6390)
        p = r.pubsub()
        with pytest.raises(redis.ConnectionError):
            p.subscribe('foo')


class TestPubSubPubSubSubcommands(object):

    @skip_if_server_version_lt('2.8.0')
    def test_pubsub_channels(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        p.subscribe('foo', 'bar', 'baz', 'quux')
        channels = sorted(r.pubsub_channels())
        assert channels == ['bar', 'baz', 'foo', 'quux']

    @skip_if_server_version_lt('2.8.0')
    def test_pubsub_numsub(self, r):
        p1 = r.pubsub(ignore_subscribe_messages=True)
        p1.subscribe('foo', 'bar', 'baz')
        p2 = r.pubsub(ignore_subscribe_messages=True)
        p2.subscribe('bar', 'baz')
        p3 = r.pubsub(ignore_subscribe_messages=True)
        p3.subscribe('baz')

        channels = [('foo', 1), ('bar', 2), ('baz', 3)]
        assert channels == r.pubsub_numsub('foo', 'bar', 'baz')

    @skip_if_server_version_lt('2.8.0')
    def test_pubsub_numpat(self, r):
        p = r.pubsub(ignore_subscribe_messages=True)
        p.psubscribe('*oo', '*ar', 'b*z')
        assert r.pubsub_numpat() == 3
