__author__ = 'Matej'

in_file = open (r'd:\temp\EPSG2WKT.TXT')
epsg_dict = {}
for line in in_file:
    # epsg_code, epsg_name = None, None
    if line.startswith('EPSG'):
        epsg_code = int(line[5:-1])
        # print epsg_code
    elif line.startswith('PROJCS') or line.startswith('GEOGCS'):
        epsg_name = line.split('"')[1] + ' (EPSG: %i )' % epsg_code
        # epsg_dict[epsg_code] = epsg_name
        epsg_dict[epsg_name] = epsg_code
    else:
        print 'Error EPSG code: %i, name: %s' % (epsg_code, epsg_name)


print epsg_dict