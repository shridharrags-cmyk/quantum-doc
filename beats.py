# Beat sheet: (image key, weight in seconds, motion, caption/source)
# motion = dict(z=(z0,z1), f=(fx,fy), pan=(px,py))

def P(k, w, z=(1.0, 1.06), f=(0.5, 0.5), pan=(0, 0), cap=None, src=None, kind="photo"):
    return dict(k=k, w=w, z=z, f=f, pan=pan, cap=cap, src=src, kind=kind)

BEATS = {}

BEATS[0] = [
    P("planck", 16, (1.02, 1.10), (0.5, 0.38), src="Max Planck, 1910 · Rudolf Dührkoop · Public domain"),
    P("filament", 9, (1.04, 1.12), (0.5, 0.5)),
    P("solvay", 21, (1.00, 1.07), (0.5, 0.5), src="Fifth Solvay Conference, Brussels, 1927 · Benjamin Couprie · Public domain"),
    P("einstein", 15, (1.06, 1.00), (0.5, 0.4), src="Albert Einstein · Public domain"),
    P("planck", 12, (1.10, 1.02), (0.62, 0.42)),
    P("fridge_chand", 14, (1.02, 1.10), (0.5, 0.72), cap="a dilution refrigerator", src="Onri Jay Benally · CC BY 4.0"),
    P("chip_200", 13, (1.10, 1.00), (0.5, 0.5), src="200-qubit superconducting processor · Onri Jay Benally · CC BY 4.0"),
]

BEATS[1] = [
    P("planck", 12, (1.00, 1.08), (0.45, 0.42)),
    P("filament", 7, (1.06, 1.14), (0.5, 0.45)),
    P("einstein", 10, (1.02, 1.09), (0.5, 0.38)),
    P("oscilloscope", 7, (1.05, 1.12), (0.5, 0.5), cap="the photoelectric effect, measured", src="Tektronix 475A · CC BY-SA 3.0"),
    P("bohr", 12, (1.08, 1.00), (0.48, 0.38)),
    P("hydspec", 11, (1.00, 1.06), (0.5, 0.5), cap="hydrogen · the visible spectrum", src="Wikimedia Commons · CC0"),
    P("solvay", 9, (1.12, 1.04), (0.35, 0.45)),
    P("diffraction", 11, (1.00, 1.09), (0.5, 0.5), cap="electron diffraction", src="Wikimedia Commons"),
    P("heisenberg", 12, (1.02, 1.10), (0.5, 0.36)),
    P("helgoland", 9, (1.08, 1.00), (0.5, 0.5), cap="Helgoland, North Sea", src="Ralf Roletschek · CC BY-SA 3.0"),
    P("schrodinger", 12, (1.04, 1.12), (0.5, 0.36)),
    P("born", 11, (1.06, 0.99), (0.5, 0.4)),
    P("solvay", 13, (1.00, 1.10), (0.5, 0.52)),
    P("einstein", 12, (1.10, 1.02), (0.55, 0.42)),
    P("bell", 11, (1.02, 1.10), (0.5, 0.38)),
    P("clauser", 10, (1.06, 1.12), (0.5, 0.38)),
    P("aspect", 10, (1.04, 1.12), (0.5, 0.4)),
    P("zeilinger", 10, (1.08, 1.00), (0.5, 0.4)),
    P("blackhole", 9, (1.06, 1.00), (0.5, 0.5), src="Event Horizon Telescope · CC BY 4.0"),
]

BEATS[2] = [
    P("landauer", 13, (1.02, 1.10), (0.5, 0.4)),
    P("punched", 8, (1.08, 1.00), (0.5, 0.5)),
    P("eniac", 11, (1.00, 1.08), (0.5, 0.5), src="ENIAC, 1946 · U.S. Army · Public domain"),
    P("colossus", 8, (1.06, 1.12), (0.5, 0.5), src="Colossus, Bletchley Park · Public domain"),
    P("shannon", 9, (1.04, 1.10), (0.5, 0.38)),
    P("benioff", 10, (1.02, 1.09), (0.5, 0.4)),
    P("feynman", 14, (1.00, 1.08), (0.5, 0.38), src="Richard Feynman, Nobel Prize 1965 · Public domain"),
    P("cambridge", 7, (1.08, 1.00), (0.5, 0.5)),
    P("deutsch", 11, (1.04, 1.12), (0.5, 0.4)),
    P("shor", 13, (1.02, 1.10), (0.5, 0.38)),
    P("difference", 7, (1.06, 1.12), (0.5, 0.5)),
    P("sliderule", 7, (1.10, 1.00), (0.5, 0.5)),
    P("fridge_open", 9, (1.00, 1.07), (0.5, 0.55)),
    P("chip_wire", 9, (1.12, 1.00), (0.5, 0.5), src="Onri Jay Benally · CC BY 4.0"),
]

BEATS[3] = [
    P("fridge_gold", 15, (1.00, 1.09), (0.5, 0.5), cap="10 millikelvin", src="Onri Jay Benally · CC BY 4.0"),
    P("fridge_open", 12, (1.10, 1.00), (0.5, 0.55)),
    P("cables", 11, (1.02, 1.10), (0.5, 0.5), cap="every line is a filter", src="Onri Jay Benally · CC BY 4.0"),
    P("chip_cross", 10, (1.00, 1.12), (0.5, 0.5)),
    P("iontrap", 12, (1.04, 1.12), (0.5, 0.5), cap="a trapped-ion processor", src="NIST · Public domain"),
    P("ibmq", 13, (1.00, 1.08), (0.5, 0.4), src="IBM Quantum System One · Onri Jay Benally · CC BY 4.0"),
    P("cleanroom", 9, (1.06, 1.00), (0.5, 0.45)),
    P("wafer", 9, (1.10, 1.00), (0.5, 0.5)),
    P("sycamore", 14, (1.02, 1.10), (0.5, 0.5), cap="Sycamore, 53 qubits", src="Google · CC BY 3.0"),
    P("google", 8, (1.08, 1.00), (0.5, 0.5)),
    P("summit", 9, (1.00, 1.08), (0.5, 0.5), cap="a classical supercomputer", src="Oak Ridge National Laboratory"),
    P("chip_100", 12, (1.12, 1.00), (0.5, 0.5)),
]

BEATS[4] = [
    P("chip_wire", 10, (1.02, 1.10), (0.5, 0.5)),
    P("surface", 16, kind="proc", cap="the surface code"),
    P("amp", 10, (1.00, 1.10), (0.5, 0.5)),
    P("chip_cross", 9, (1.10, 1.00), (0.5, 0.5)),
    P("fridge_sys", 10, (1.04, 1.12), (0.5, 0.5)),
    P("sycamore", 8, (1.06, 0.99), (0.45, 0.5)),
    P("willow_chart", 15, kind="proc", cap="Willow · logical error per cycle"),
    P("chip_200", 10, (1.00, 1.10), (0.5, 0.5)),
    P("datacenter", 8, (1.08, 1.00), (0.5, 0.5)),
    P("frontier", 9, (1.02, 1.10), (0.5, 0.5), cap="Frontier · 1.35 exaflops"),
    P("wafer", 10, (1.10, 1.00), (0.5, 0.5)),
]

BEATS[5] = [
    P("ibmq", 12, (1.00, 1.08), (0.5, 0.42)),
    P("iontrap", 11, (1.06, 1.12), (0.5, 0.5)),
    P("optlattice", 10, (1.00, 1.08), (0.5, 0.5), cap="atoms in an optical lattice", src="NIST"),
    P("wafer", 8, (1.08, 1.00), (0.5, 0.5)),
    P("fiber", 10, (1.02, 1.10), (0.5, 0.5)),
    P("microsoft", 11, (1.00, 1.08), (0.5, 0.5), cap="Redmond, February 2025"),
    P("chip_24", 12, (1.06, 1.14), (0.5, 0.5)),
    P("dwave", 9, (1.04, 1.12), (0.5, 0.5)),
    P("honeywell", 8, (1.08, 1.00), (0.5, 0.5)),
    P("stockholm", 9, (1.00, 1.08), (0.5, 0.5), cap="Stockholm"),
    P("datacenter", 9, (1.10, 1.00), (0.5, 0.5)),
    P("gps", 9, (1.04, 1.12), (0.5, 0.5)),
    P("fiber", 10, (1.10, 1.00), (0.5, 0.5)),
    P("blackhole", 9, (1.00, 1.08), (0.5, 0.5)),
]

BEATS[6] = [
    P("hydroden", 14, (1.00, 1.08), (0.5, 0.5), cap="a molecule is a quantum system"),
    P("cleanroom2", 10, (1.06, 1.12), (0.5, 0.5)),
    P("wafer", 9, (1.10, 1.00), (0.5, 0.5)),
    P("summit", 8, (1.00, 1.08), (0.5, 0.5)),
    P("fridge_gold", 11, (1.08, 1.00), (0.5, 0.5)),
    P("milkyway", 12, (1.00, 1.07), (0.5, 0.5), src="ESO · CC BY 4.0"),
    P("obsuniverse", 10, (1.04, 1.12), (0.5, 0.5)),
    P("planck", 14, (1.06, 0.99), (0.5, 0.4)),
    P("chip_200", 12, (1.00, 1.12), (0.5, 0.5)),
    P("stars", 12, (1.00, 1.06), (0.5, 0.5)),
]
