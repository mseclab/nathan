def print_debug(msg):
    s1 = ""
    format = ';'.join([str(32)])
    s1 = '\x1b[%sm%s\x1b[0m' % (format, msg)
    print s1

def print_info(msg):
    s1 = ""
    format = ';'.join([str(34)])
    s1 = '\x1b[%sm%s\x1b[0m' % (format, msg)
    print s1

def print_error(msg):
    s1 = ""
    format = ';'.join([str(31)])
    s1 = '\x1b[%sm%s\x1b[0m' % (format, msg)
    print s1

def print_format_table():
    for style in xrange(8):
        for fg in xrange(30,38):
            s1 = ''
            for bg in xrange(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print s1

    print '\n'
    s1 = ""
    format = ';'.join([str(32)])
    s1 = '\x1b[%sm %s wewe \x1b[0m' % (format, format)
    print s1+"wewe"
