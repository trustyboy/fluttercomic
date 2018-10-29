# -*- coding:utf-8 -*-
"""
HTMLTEMPLATE 是paypal充值页面模板
"""
from simpleutil.utils import encodeutils

HTMLTEMPLATE = '''
<script src="https://www.paypalobjects.com/api/checkout.js"></script>

<div id="paypal-button"></div>

<script>

    paypal.Button.render({
        style: {'label': 'buynow', 'size': 'responsive'},
        env: 'sandbox',
        payment: function (data, actions) {
            return actions.request({
                    method: "post",
                    url: '/n1.0/fluttercomic/orders/platforms/paypal',
                    json: {money: %(money)d, uid: %(uid)d, oid: '%(oid)d', cid: %(cid)d, chapter: %(chapter)d},
                })
                .then(function (res) {
                    return res.data[0].paypal.paymentID;
                });
        },
        onAuthorize: function (data, actions) {
            return actions.request({
                    method: "post",
                    url: '/n1.0/fluttercomic/orders/callback/paypal/%(oid)d',
                    json: {paypal: { paymentID: data.paymentID, payerID: data.payerID}, uid: %(uid)d},
                })
                .then(function (res) {
                    window.postMessage(JSON.stringify({paypal: { paymentID: data.paymentID, payerID: data.payerID}, oid: %(oid)d}))
                    // 3. Show the buyer a confirmation message.
                });
        }
    }, '#paypal-button');
</script>
'''


def html(oid, uid, cid, chapter, money):
    # Javascript json oid error
    buf = HTMLTEMPLATE % {'oid': oid,
                          'uid': uid, 'money': money,
                          'cid': cid, 'chapter': chapter}
    return encodeutils.safe_decode(buf, 'utf-8')

def translate(money):
    return money*10, 0