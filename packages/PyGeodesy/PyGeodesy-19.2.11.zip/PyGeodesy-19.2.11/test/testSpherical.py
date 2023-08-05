
# -*- coding: utf-8 -*-

# Test spherical earth model functions and methods.

__all__ = ('Tests',)
__version__ = '19.02.10'

from base import isWindows
from testLatLon import Tests as _TestsLL
from testVectorial import Tests as _TestsV

from pygeodesy import F_D, F_DMS, classname, lonDMS

# <http://GeographicLib.SourceForge.io/html/python/examples.html>
Antarctica = ((-63.1, -58),
              (-72.9, -74),
              (-71.9,-102),
              (-74.9,-102),
              (-74.3,-131),
              (-77.5,-163),
              (-77.4, 163),
              (-71.7, 172),
              (-65.9, 140),
              (-65.7, 113),
              (-66.6,  88),
              (-66.9,  59),
              (-69.8,  25),
              (-70.0,  -4),
              (-71.0, -14),
              (-77.3, -33),
              (-77.9, -46),
              (-74.7, -61))  # open


class Tests(_TestsLL, _TestsV):

    def testSpherical(self, module, Sph=True):  # MCCABE 13

        self.subtitle(module, 'Spherical')

        LatLon, Vct = module.LatLon, not Sph

        p = LatLon(51.8853, 0.2545)
        self.test('isSpherical', p.isSpherical, True)
        self.test('isEllipsoidal', p.isEllipsoidal, False)

        q = LatLon(49.0034, 2.5735)
        self.test('isSpherical', q.isSpherical, True)
        self.test('isEllipsoidal', q.isEllipsoidal, False)

        i = p.intersection(108.55, q, 32.44)
        self.test('intersection1', i.toStr(F_D), '50.907608°N, 004.508575°E')  # 50.9076°N, 004.5086°E  # Trig
        self.test('intersection1', i.toStr(F_DMS), '50°54′27.39″N, 004°30′30.87″E')
        self.test('intersection1', isinstance(i, LatLon), True)

        REO = LatLon(42.600, -117.866)
        BKE = LatLon(44.840, -117.806)
        i = REO.intersection(51, BKE, 137)
        self.test('intersection2', isinstance(i, LatLon), True)
        self.test('intersection2', i.toStr(F_D), '43.5719°N, 116.188757°W')  # 43.572°N, 116.189°W
        self.test('intersection2', i.toStr(F_DMS), '43°34′18.84″N, 116°11′19.53″W')

        # <http://GitHub.com/ChrisVeness/geodesy/issues/46>
        p = LatLon(51.8853, 0.2545)
        q = LatLon(51.8763, 0.2545)  # identical lon
        i = p.intersection(110.8878, q, 54.4525)
        self.test('intersection3', i, '51.882166°N, 000.267801°E')  # 51°52′55.8″N, 000°16′04.08″E?

        p = LatLon(+30, 0)
        q = LatLon(-30, 0)  # indential, zero lon
        i = p.intersection(135, q, 45)
        self.test('intersection4', i, '00.0°N, 026.565051°E', known=isWindows)

        p = LatLon(0, -30)
        q = LatLon(0, +30)  # identical, zero lat
        i = p.intersection(45, q, 315)
        self.test('intersection5', i, '26.565051°N, 000.0°W', known=isWindows)

        # <http://GitHub.com/ChrisVeness/geodesy/blob/master/test/latlon-vectors-tests.js>
        STN = LatLon(51.8853, 0.2545)
        CDG = LatLon(49.0034, 2.5735)
        i = STN.intersection(108.547, CDG, 32.435)
        self.test('intersection6', i, '50.907809°N, 004.50841°E')  # 50.9078°N, 004.5084°E

        # <http://GitHub.com/ChrisVeness/geodesy/blob/master/test/latlon-vectors-tests.js>
        # <http://GitHub.com/ChrisVeness/geodesy/blob/master/test/latlon-spherical-tests.js>
        N, E, S, W, p, q = 0, 90, 180, 270, LatLon(0, 1), LatLon(1, 0)
        self.test('toward 1,1 N,E nearest',        p.intersection(N, q, E), '00.999848°N, 001.0°E')
        self.test('toward 1,1 E,N nearest',        q.intersection(E, p, N), '00.999848°N, 001.0°E')
        self.test('toward 1,1 N,E antipodal',      LatLon(2, 1).intersection(N, q, E), '00.999848°S, 179.0°W')
        self.test('toward/away 1,1 N,W antipodal', p.intersection(N, q, W), '00.999848°S, 179.0°W', known=Sph)
        self.test('toward/away 1,1 W,N antipodal', q.intersection(W, p, N), '00.999848°S, 179.0°W')
        self.test('toward/away 1,1 S,E antipodal', p.intersection(S, q, E), '00.999848°S, 179.0°W')
        self.test('toward/away 1,1 E,S antipodal', q.intersection(E, p, S), '00.999848°S, 179.0°W', known=Sph)
        self.test('away 1,1 S,W antipodal',        p.intersection(S, q, W), '00.999848°S, 179.0°W')
        self.test('away 1,1 W,S antipodal',        q.intersection(W, p, S), '00.999848°S, 179.0°W')
        self.test('1E/90E N,E antipodal',          p.intersection(N, LatLon(1, 90), E), '00.017454°S, 179.0°W', known=Sph)
        self.test('1E/90E N,E nearest',            p.intersection(N, LatLon(1, 92), E), '00.017454°N, 179.0°W')

        # <http://GitHub.com/ChrisVeness/geodesy/blob/master/test/latlon-vectors-tests.js>
        p, r = LatLon(1, 3), LatLon(2, 2)
        self.test('brng+end 1a', q.intersection(p, r, S), '01.000305°N, 002.0°E')
        self.test('brng+end 1b', r.intersection(S, q, p), '01.000305°N, 002.0°E')
        self.test('brng+end 2a', q.intersection(p, r, N), '01.000305°S, 178.0°W')
        self.test('brng+end 2b', r.intersection(N, q, p), '01.000305°S, 178.0°W')

        i = LatLon(1, 1).intersection(LatLon(2, 2), LatLon(1, 4), LatLon(2, 3))
        self.test('intersection7', i, '02.499372°N, 002.5°E')  # 02.4994°N, 002.5°E'

        p = LatLon(0, 0)
        self.test('maxLat0',  p.maxLat( 0), '90.0')
        self.test('maxLat1',  p.maxLat( 1), '89.0')
        self.test('maxLat90', p.maxLat(90),  '0.0')

        if hasattr(LatLon, 'crossingParallels'):
            ps = p.crossingParallels(LatLon(60, 30), 30)
            t = ', '.join(map(lonDMS, ps))
            self.test('crossingParallels', t, '009°35′38.65″E, 170°24′21.35″E')

        if hasattr(LatLon, 'isenclosedBy'):
            p = LatLon(45.1, 1.1)

            b = LatLon(45, 1), LatLon(45, 2), LatLon(46, 2), LatLon(46, 1)
            for _ in self.testiter():
                self.test('isenclosedBy', p.isenclosedBy(b), True)

            b = LatLon(45, 1), LatLon(45, 3), LatLon(46, 2), LatLon(47, 3), LatLon(47, 1)
            for _ in self.testiter():
                try:
                    self.test('isenclosedBy', p.isenclosedBy(b), True)  # Nvector
                except ValueError as x:
                    t = ' '.join(str(x).split()[:3] + ['...)'])
                    self.test('isenclosedBy', t, 'non-convex: (%s(45°00′00.0″N, 001°00′00.0″E), ...)' % (classname(p),))

        p = LatLon(51.127, 1.338)
        q = LatLon(50.964, 1.853)
        b = p.rhumbBearingTo(q)
        self.test('rhumbBearingTo', b, 116.722, fmt='%.3f')  # 116.7

        d = p.rhumbDestination(40300, 116.7)
        self.test('rhumbDestination', d, '50.964155°N, 001.853°E')  # 50.9642°N, 001.8530°E
        self.test('rhumbDestination', isinstance(d, LatLon), True)

        d = p.rhumbDistanceTo(q)
        self.test('rhumbDistanceTo', d, 40307.8, fmt='%.1f')  # XXX 40310 ?

        m = p.rhumbMidpointTo(q)
        self.test('rhumbMidpointo', m, '51.0455°N, 001.595727°E')
        self.test('rhumbMidpointo', isinstance(m, LatLon), True)

        b = LatLon(45, 1), LatLon(45, 2), LatLon(46, 2), LatLon(46, 1)
        self.test('areaOf', module.areaOf(b), '8.6660587507e+09', fmt='%.10e')  # 8666058750.718977

        c = LatLon(0, 0), LatLon(1, 0), LatLon(0, 1)
        self.test('areaOf', module.areaOf(c), '6.18e+09', fmt='%.2e')

        if hasattr(module, 'nearestOn2'):
            c, d = module.nearestOn2(p, b)
            self.test('nearestOn2', c, '46.000996°N, 001.353049°E' if Vct else '46.0°N, 001.369324°E')
            self.test('nearestOn2', d, '569987.49' if Vct else '570101.83', fmt='%.2f')
            d = p.distanceTo(c)
            self.test('distanceTo', d, '569987.49' if Vct else '570101.82', fmt='%.2f')

            p = LatLon(47, 3)
            c, d = module.nearestOn2(p, b)
            self.test('nearestOn2', c, '46.0°N, 002.0°E' if Vct else '46.0°N, 002.0°E')
            self.test('nearestOn2', d, '134989.80' if Vct else '134992.48', fmt='%.2f')
            d = p.distanceTo(c)
            self.test('distanceTo', d, '134989.80' if Vct else '134989.80', fmt='%.2f')

            p = LatLon(45, 2)
            b = LatLon(45, 1), LatLon(47, 3)
            if Vct:
                c, d = module.nearestOn2(p, b)
                self.test('nearestOn2', c, '45.330691°N, 001.318551°E')
                self.test('distance', d, '64856.28', fmt='%.2f')
            else:
                c, d, a = p.nearestOn3(b, adjust=False)
                self.test('nearestOn3', c, '45.5°N, 001.5°E')
                self.test('distance', d, '78626.79', fmt='%.2f')
                self.test('angle', a, '315.00', fmt='%.2f')
                a = p.compassAngleTo(c, adjust=False)
                self.test('compassAngleTo', a, '315.00', fmt='%.2f')
                c, d, a = p.nearestOn3(b, adjust=True)
                self.test('nearestOn3', c, '45.331319°N, 001.331319°E')
                self.test('distance', d, '64074.48', fmt='%.2f')
                self.test('angle', a, '305.10', fmt='%.2f')
            d = p.distanceTo(c)
            self.test('distanceTo', d, '64856.28' if Vct else '64074.12', fmt='%.2f')
            a = p.compassAngleTo(c)  # adjust=True
            self.test('compassAngleTo', a, '304.54' if Vct else '305.10', fmt='%.2f')
            # TrigTrue vs Nvector closests
            p = LatLon(45.330691, 001.318551)
            d = p.distanceTo(LatLon(45.331319, 001.331319))
            self.test('difference', d, '1000.53', fmt='%.2f')  # PYCHOK test attr?

            if Sph:  # check nearestOn2/3 with closest on the segment
                b = LatLon(0, 1), LatLon(2, 3), LatLon(4, 5), LatLon(6, 7), LatLon(8, 9)
                for i in range(8):
                    p = LatLon(i + 2, i)
                    c, d, a = p.nearestOn3(b, adjust=False)
                    q = LatLon(p.lat - 1.5, p.lon + 1.5)
                    self.test('nearestOn3', c.toStr(F_D, prec=6), q.toStr(F_D, prec=6))
                    self.test('distance', d, '235880.385', fmt='%.3f')
                    self.test('angle', a, '135.00', fmt='%.2f')

        if hasattr(module, 'ispolar'):
            p = LatLon(85, 90), LatLon(85, 0), LatLon(85, -90), LatLon(85, -180)
            for _ in self.testiter():
                self.test('ispolar', module.ispolar(p), 'True')  # PYCHOK test attr?
            p = LatLon(85, 90), LatLon(85, 0), LatLon(85, -180)
            for _ in self.testiter():
                self.test('ispolar', module.ispolar(p), 'True', known=True)  # PYCHOK test attr?
            p = [LatLon(*ll) for ll in Antarctica]  # PYCHOK test attr?
            for _ in self.testiter():
                self.test('ispolar', module.ispolar(p), 'True', known=Vct)  # PYCHOK test attr?

        if hasattr(LatLon, 'nearestOn'):
            # <http://GitHub.com/mrJean1/PyGeodesy/issues/25>
            a = LatLon(1, 1, height=100)
            b = LatLon(2, 2, height=200)
            t = LatLon(1, 2).nearestOn(a, b).toStr(form=F_D, prec=1)
            self.test('nearestOn', t, '01.5°N, 001.5°E, +149.99m')  # PYCHOK test attr?


if __name__ == '__main__':

    from pygeodesy import sphericalNvector as Nv, \
                          sphericalTrigonometry as Trig

    t = Tests(__file__, __version__)

    t.testLatLon(Nv, Sph=True)
    t.testVectorial(Nv)
    t.testSpherical(Nv, Sph=False)

    t.testLatLon(Trig, Sph=True)
    t.testSpherical(Trig, Sph=True)

    t.results()
    t.exit()
