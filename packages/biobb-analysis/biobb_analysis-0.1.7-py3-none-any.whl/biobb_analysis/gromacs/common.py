""" Common functions for package biobb_analysis.gromacs """
import os.path
from biobb_common.tools import file_utils as fu


def check_energy_path(path):
	""" Checks energy input file """ 
	if not os.path.exists(path):
		raise SystemExit('Unexisting energy input file')
	filename, file_extension = os.path.splitext(path)
	if not is_valid_energy(file_extension[1:]):
		raise SystemExit('Format %s in energy input file is not compatible' % file_extension[1:])
	return path

def check_input_path(path):
	""" Checks input structure file """ 
	if not os.path.exists(path):
		raise SystemExit('Unexisting structure input file')
	filename, file_extension = os.path.splitext(path)
	if not is_valid_structure(file_extension[1:]):
		raise SystemExit('Format %s in structure input file is not compatible' % file_extension[1:])
	return path

def check_traj_path(path):
	""" Checks input structure file """ 
	if not os.path.exists(path):
		raise SystemExit('Unexisting trajectory input file')
	filename, file_extension = os.path.splitext(path)
	if not is_valid_trajectory(file_extension[1:]):
		raise SystemExit('Format %s in trajectory input file is not compatible' % file_extension[1:])
	return path

def check_out_xvg_path(path):
	""" Checks if output folder exists and format is xvg """
	if not os.path.exists(os.path.dirname(path)):
		raise SystemExit('Unexisting output folder')
	filename, file_extension = os.path.splitext(path)
	if not is_valid_xvg(file_extension[1:]):
		raise SystemExit('Format %s in output file is not compatible' % file_extension[1:])
	return path

def check_out_pdb_path(path):
	""" Checks if output folder exists and format is xvg """
	if not os.path.exists(os.path.dirname(path)):
		raise SystemExit('Unexisting output folder')
	filename, file_extension = os.path.splitext(path)
	if not is_valid_structure(file_extension[1:]):
		raise SystemExit('Format %s in output file is not compatible' % file_extension[1:])
	return path

def check_conf(path):
	""" Checks configuration file """
	if not os.path.exists(path):
		raise SystemExit('Unexisting configuration file')
	return path

def get_default_value(key):
	""" Gives default values according to the given key """
	default_values = {
		"instructions_file": "instructions.in",
		"gmx_path": "gmx",
		"terms": ["Potential"],
		"selection": "Protein-H"
	}

	return default_values[key]

def get_binary_path(properties, type):
	""" Gets binary path """
	return properties.get(type, get_default_value(type))

def get_terms(properties):
	""" Gets energy terms """
	terms = properties.get('terms', dict())
	if not terms or not isinstance(terms, list):
		raise SystemExit('No terms provided or incorrect format')
	if not is_valid_term(terms):
		raise SystemExit('Incorrect terms provided')
	return properties.get('terms', '')

def get_selection(properties):
	""" Gets selection items """
	selection = properties.get('selection', get_default_value('selection'))
	if not selection:
		raise SystemExit('No selection provided or incorrect format')
	if not is_valid_selection(selection):
		raise SystemExit('Incorrect selection provided')
	return selection

def get_xvg(properties):
	""" Gets xvg """
	xvg = properties.get('xvg', 'none')
	if not is_valid_xvg_param(xvg):
		raise SystemExit('Incorrect xvg provided')
	return xvg

def is_valid_structure(ext):
	""" Checks if structure format is compatible with GROMACS """
	formats = ['tpr', 'gro', 'g96', 'pdb', 'brk', 'ent']
	return ext in formats

def is_valid_trajectory(ext):
	""" Checks if trajectory format is compatible with GROMACS """
	formats = ['xtc', 'trr', 'cpt', 'gro', 'g96', 'pdb', 'tng']
	return ext in formats

def is_valid_energy(ext):
	""" Checks if energy format is compatible with GROMACS """
	formats = ['edr']
	return ext in formats

def is_valid_xvg(ext):
	""" Checks if file is XVG """
	formats = ['xvg']
	return ext in formats

def is_valid_xvg_param(ext):
	""" Checks xvg parameter """
	formats = ['xmgrace', 'xmgr', 'none']
	return ext in formats

def is_valid_term(iterms):
	""" Checks if term is correct """
	cterms = ['Angle', 'Proper-Dih.', 'Improper-Dih.', 'LJ-14', 'Coulomb-14', 'LJ-(SR)', 'Coulomb-(SR)', 'Coul.-recip.', 'Position-Rest.', 'Potential', 'Kinetic-En.', 'Total-Energy', 'Temperature', 'Pressure', ' Constr.-rmsd', 'Box-X', 'Box-Y', ' Box-Z', 'Volume', 'Density', 'pV', 'Enthalpy', 'Vir-XX', 'Vir-XY', 'Vir-XZ', 'Vir-YX', 'Vir-YY', 'Vir-YZ', 'Vir-ZX', 'Vir-ZY', 'Vir-ZZ', 'Pres-XX', 'Pres-XY', 'Pres-XZ', 'Pres-YX', 'Pres-YY', 'Pres-YZ', 'Pres-ZX', 'Pres-ZY', 'Pres-ZZ', '#Surf*SurfTen', 'Box-Vel-XX', 'Box-Vel-YY', 'Box-Vel-ZZ', 'Mu-X', 'Mu-Y', 'Mu-Z', 'T-Protein', 'T-non-Protein', 'Lamb-Protein', 'Lamb-non-Protein']
	return all(elem in cterms for elem in iterms)

def is_valid_selection(ext):
	""" Checks if selection is correct """
	formats = ['System', 'Protein', 'Protein-H', 'C-alpha', 'Backbone', 'MainChain', 'MainChain+Cb', 'MainChain+H', 'SideChain', 'SideChain-H', 'Prot-Masses', 'non-Protein', 'Water', 'SOL', 'non-Water', 'Ion', 'NA', 'CL', 'Water_and_ions']
	return ext in formats
