import time
from math import floor
def gen_gga(time_t, lat, lat_pole, lng, lng_pole, fix_quality, num_sats, hdop, alt_m, geoidal_sep_m, dgps_age_sec, dgps_ref_id):
  hhmmssss = '%02d%02d%02d%s' % (time_t.tm_hour, time_t.tm_min, time_t.tm_sec, '.%02d' if 0 != 0 else '')

  lat_abs = abs(lat)
  lat_deg = lat_abs
  lat_min = (lat_abs - floor(lat_deg)) * 60
  lat_sec = round((lat_min - floor(lat_min)) * 1000)
  lat_pole_prime = ('S' if lat_pole == 'N' else 'N') if lat < 0 else lat_pole
  lat_format = '%02d%02d.%03d' % (lat_deg, lat_min, lat_sec)

  lng_abs = abs(lng)
  lng_deg = lng_abs
  lng_min = (lng_abs - floor(lng_deg)) * 60
  lng_sec = round((lng_min - floor(lng_min)) * 1000)
  lng_pole_prime = ('W' if lng_pole == 'E' else 'E') if lng < 0 else lng_pole
  lng_format = '%03d%02d.%03d' % (lng_deg, lng_min, lng_sec)

  dgps_format = '%s,%s' % ('%.1f' % dgps_age_sec if dgps_age_sec is not None else '', '%04d' % dgps_ref_id if dgps_ref_id is not None else '')

  str = 'GPGGA,%s,%s,%s,%s,%s,%d,%02d,%.1f,%.1f,M,%.1f,M,%s' % (hhmmssss, lat_format, lat_pole_prime, lng_format, lng_pole_prime, fix_quality, num_sats, hdop, alt_m, geoidal_sep_m, dgps_format)
  crc = 0
  for c in str:
    crc = crc ^ ord(c)
  crc = crc & 0xFF

  return '$%s*%0.2X' % (str, crc)
import random
def get_nmea():
    return gen_gga(time.gmtime(), round(random.uniform(-180.000000, 180.000000), 6), 'N', round(random.uniform(-180.000000, 180.000000), 6), 'W', 1, 7, 1.5, 280.2, -34, 0, 0)


