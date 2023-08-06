import os
import glob
import shutil
import pytest
import oommfc as oc
from .test_driver import TestDriver


class TestTimeDriver(TestDriver):
    def test_script(self):
        driver = oc.TimeDriver()
        t = 1e-9
        n = 120
        script = driver._script(self.system, t=t, n=n)

        assert script[0] == "#"
        assert script[-1] == "1"
        assert script.count("#") == 5
        assert script.count("Specify") == 3
        assert script.count("Destination") == 3
        assert script.count("Schedule") == 2
        assert script.count("mmArchive") == 3
        assert script.count("Stage") == 2

        assert "Oxs_RungeKuttaEvolve" in script
        assert "Oxs_TimeDriver" in script
        assert "Oxs_FileVectorField" in script

        lines = script.split("\n")
        alpha = self.system.dynamics.damping.alpha
        assert lines[2] == "  alpha {}".format(alpha)
        gamma = self.system.dynamics.precession.gamma
        assert lines[3] == "  gamma_G {}".format(gamma)

    @pytest.mark.oommf
    def test_drive(self):
        md = oc.TimeDriver()

        md.drive(self.system, t=0.1e-9, n=10, overwrite=True)

        assert os.path.exists("tds")
        dirname = os.path.join("tds", "drive-{}".format(self.system.drive_number-1))
        miffilename = os.path.join(dirname, "tds.mif")
        assert os.path.isfile(miffilename)

        omf_files = list(glob.iglob(os.path.join(dirname, '*.omf')))
        odt_files = list(glob.iglob(os.path.join(dirname, '*.odt')))

        assert len(omf_files) == 11
        omffilename = os.path.join(dirname, "m0.omf")
        assert omffilename in omf_files

        assert len(odt_files) == 1

        shutil.rmtree("tds")

    def test_drive_exception(self):
        md = oc.TimeDriver()
        with pytest.raises(ValueError):
            md.drive(self.system, t=-0.1e-9, n=10)
        with pytest.raises(ValueError):
            md.drive(self.system, t=0.1e-9, n=-10)

    def test_script_missing_terms(self):
        # Missing Gilbert damping alpha
        self.system.dynamics = oc.Precession(gamma=2.2)
        td = oc.TimeDriver()
        script = td._script(self.system, t=1e-9, n=20)
        assert "alpha 0" in script
        assert "gamma_G 2.2" in script

        # Missing gamma
        self.system.dynamics = oc.Damping(alpha=5)
        td = oc.TimeDriver()
        script = td._script(self.system, t=1e-9, n=20)
        assert "alpha 5" in script
        assert "gamma_G 221100" in script
