import unittest
import pylzmat

TEST = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur'
        ' viverra quis lacus sit amet bibendum. Integer pretium vel libero '
        'sollicitudin lobortis. Nunc eu nibh a quam hendrerit condimentum. '
        'Aenean tristique cursus tincidunt. Nam eleifend mi in sapien efficitur, '
        'non sagittis diam gravida. Nulla auctor interdum tortor eget laoreet. '
        'Mauris ullamcorper commodo dolor nec tempor. Vestibulum ante ipsum '
        'primis in faucibus orci luctus et ultrices posuere cubilia Curae; Cras '
        'sollicitudin orci eget mi maximus, pretium dapibus ipsum ultricies. Nam '
        'sit amet commodo lorem, finibus vestibulum tortor. Maecenas molestie dui '
        'vitae diam bibendum finibus. Aenean a mattis erat, sit amet feugiat sem.')

TEST_ENC = ('L\x00orem ips\x00um dolor\x00 sit ame\x00t, conse\x00ctetur '
            'a\x00dipiscin\x00g elit. \x02Curabi4a\x07\x90fW&\'\x17\x06\x12\x07'
            'P\x976\x07\xc2\x166V\x074gh biben\x00dum. Int\x00eger pre ti\xd8`W'
            '\xc6\x06\xc2\x06\xa8\x03ro soll ic\x96@\x96\xe6\x06\xc2\x06\xf0&'
            '\xf6&G\x976\xe7\x02\x00\xe2T\xe76\x06RV\'\x00\xe2\x96&\x86\x06\xc2'
            '\x1ba\x11m h\x9a W&\xc7\x0b\x819\x00diment\xb8\x01\x10T\xe6V\x16'
            '\xe6\x06B\x07 \x976G\x97\x16WWF\x002V\'7\xf7\x00@\x97&\xe06\x96FV'
            '\xe7\xf6\x05\xe0$\xa8\x07eleif\x82\x00\x02\xd1\x96\x06B\rsapi\x02'
            'en eff\xfa"\x87\xc0\x02\xe2\xf6\xa6\x12git\x88\x01\x00 didp&\x17'
            '\x86`\x97F\x16\xb6\x01\xc1\xc6\x16V\x00\x12V7Fw\x14\x90\x96\t\xd0%'
            '\xd7\n\x00\x82\x01\x1e1\x0b@W\x0f z\x19PF\rMau\x11\x00 \x82`\xd16'
            '\xf6&\x07\xb7\x0e0&\xf0\xd6\xd6\xf6F\xf6V\x1c\xe4\x06P6\x06BW\xd6'
            '\x06\xf7F \xe7\x02bUV\x06 V\x87\xc5\x86\ta\xaaP!\x04\'\x97\xc6\xd6'
            'F\x08I\x00f\xe4\xe0\x03s \x03orci l\xfe`\x01\x90\xdaP\xc7\xb6\r0V6'
            '\x07"\x00\xf76WW&W\x0e!\x86\x90\xc6\x96\x16\x16#R\xb6\x03\xf21$'
            '\x17\xf6 0\x1b\t(S \xfd\x00\x00maximus,\xbc\x1fbd\x19\x01\xcc\xe1?'
            '\xba\x93V\x86\xdf \xb1\x10\xf0)\xf6\x08\xb5\x08P\xd6\xc6\xb2\x01b'
            '\x96\x96#\x80\x06v\x89p#1\x84\t\x11ecen\x07\x00moAl:Q\x06BV\x97v5'
            '\xe0C\x17&\x01\xb3\x115S\x88\xb5(\x16f\x9c\x03\x10 R&\x17\xb6@`of'
            '\x00eugiat s\x1fem.')


class TestAnalysis(unittest.TestCase):
    def test_encode(self):
        encoded = pylzmat.encode(TEST)
        self.assertEqual(encoded, TEST_ENC)

    def test_encode_bytearray(self):
        encoded = pylzmat.encode(bytearray(TEST))
        self.assertEqual(encoded, TEST_ENC)

    def test_decode(self):
        decoded = pylzmat.decode(TEST_ENC)
        self.assertEqual(decoded, TEST)

    def test_decode_bytearry(self):
        decoded = pylzmat.decode(bytearray(TEST_ENC))
        self.assertEqual(decoded, TEST)
