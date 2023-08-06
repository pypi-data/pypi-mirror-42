"""Aux fun used in global models.

Florian Marmuse
11/12/17
"""

import numpy as np
from line_profiler import LineProfiler
from scipy.constants import pi, e, k, m_e, epsilon_0
from molar_masses import masses_dictionary
import math
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

##############
# CONVERSION #
##############


def sccm_to_persecond(sccm):
    """Convert sccm to particle per second."""
    return sccm * 4.477962E17


def persecond_to_sccm(Q):
    """Convert particle per second to sccm."""
    return Q / 4.477962E17


def power_to_volumic_power(power, volume):
    """Convert power to volumic power."""
    return power / volume


def volumic_power_to_power(volumic_power, volume):
    """Convert volumic power to power."""
    return volumic_power * volume


def find_nearest(array, value):
    """Find nearest element."""
    idx = (np.abs(array - value)).argmin()
    return array[idx]


############
# PROFILER #
############


def do_profile(follow=[]):
    def inner(func):
        def profiled_func(*args, **kwargs):
            try:
                profiler = LineProfiler()
                profiler.add_function(func)
                for f in follow:
                    profiler.add_function(f)
                profiler.enable_by_count()
                return func(*args, **kwargs)
            finally:
                profiler.print_stats()

        return profiled_func

    return inner

#
# def get_number():
#     for x in xrange(5000000):
#         yield x


##########
# PLASMA #
##########

def remove_charge(element):
    """Return the neutral element corresponding to an ion.
    Example: remove_charge('Xe')
    remove_charge('Xe^+') = 'Xe'
    """

    return element.split('^')[0]  # the whole part before the ^, or the whole part if there is not ^.


def relevant_lines(text_file):
    """Return an ordered list of the non-empty lines, without the comments.
    Example: relevant_lines('input_xenon').
    """

    with open(text_file, 'r') as input_txt:
        return [
               line.split('#')[0].strip() # the part before # of each line
               for line in input_txt.readlines()
               if (line.rstrip() is not '' and line.startswith('#') is False)
               ]  # if line not empty and not starting with #


def get(variable, section, text_file):
    """Return the value of a variable in a given section of a text file.

    Quite specific to the input file for LPP0D.
    Case sensitive.

    Example: get('R', 'THRUSTER', 'input_xenon.txt')
    """

    for line in lines_in_section(section, text_file):
        if line.startswith(variable):
            try:
                return eval(line.split('=')[1].strip())  # main return here
            except NameError:
                return line.split('=')[1].strip()

    # if nothing found:
    return 'This variable is missing.'


def list_of_reactions(text_file):
    """Return a list of the reactions, i.e. a list containing the lines of the "REACTIONS" section."""
    return lines_in_section('REACTIONS', text_file)


def reaction_elements(reaction):
    """Return a list [[reactants], [products], rate] for each reaction line you give it."""

    lhs = reaction.split('->')[0]
    reactants = [item.strip() for item in lhs.split(' + ')]

    rhs = reaction.split('->')[1].split('!')[0]
    products = [item.strip() for item in rhs.split(' + ')]
    # print(products)

    # rate = reaction.rsplit('!')[-1].strip()
    reaction_type = reaction.rsplit('!')[-1].split('&')[0].strip()

    rate_given = float(reaction.rsplit('!')[-1].split('&')[1].strip()) if '&' in reaction.rsplit('!')[-1] else False

    # return [reactants, products, rate]
    return [reactants, products, reaction_type, rate_given]


# def format_rate(rate):
#     """"format_rate('K_Xe_e_ELA(Te)') = R['Xe']['e']['ELA'].K(Te)
#     Une fonction adhoc qu'il pourrait etre bon de modifier...
#     """
#     rate = rate.split('(')[0]  # remove (Te)
#     reac1 = rate.split('_')[1]
#     reac2 = rate.split('_')[2]
#     type = rate.split('_')[3]
#     return 'R[\'{}\'][\'{}\'][\'{}\'].K(Te)'.format(reac1, reac2, type).replace('\'e\'', '\'e^-\'')

def format_rate(reaction):
    [reactants, products, type, rate_given] = reaction_elements(reaction)
    return 'R[\'{}\'][\'{}\'][\'{}\'].K(Te)'.format(reactants[0], reactants[1], type).replace('\'e\'', '\'e^-\'')


def format_energy(reaction):
    [reactants, products, type, rate_given] = reaction_elements(reaction)
    return 'R[\'{}\'][\'{}\'][\'{}\'].energy_loss'.format(reactants[0], reactants[1], type).replace('\'e\'', '\'e^-\'')

# def format_energy(rate):
#     """"format_energy('K_Xe_e_ELA(Te)') = R['Xe']['e']['ELA'].energy_loss"""
#     rate = rate.split('(')[0]  # remove (Te)
#     reac1 = rate.split('_')[1]
#     reac2 = rate.split('_')[2]
#     type = rate.split('_')[3]
#     return 'R[\'{}\'][\'{}\'][\'{}\'].energy_loss'.format(reac1, reac2, type).replace('\'e\'', '\'e^-\'')


# def reaction_type(reaction):
#     [reactants, products, rate] = reaction_elements(reaction)
#     return rate.split('(')[0].split('_')[-1]


def all_reactions(text_file):
    """Return a list of the reactions under the format [reac1_reac2_type]"""
    return [l.split('!')[-1].strip().split('(')[0][2:] for l in list_of_reactions(text_file)]


# def reac_short(reac):
#     """Return the reactants of a given reaction.
#
#     Ex: Xe_e_ela -> Xe_e
#     """
#
#     return reac.split('_')[0] + '_' + reac.split('_')[1]
#
#
# # EXAMPLE
# reac_short("Xe_e_ela")

#####################################


# def reac_type(reac):
#     """Return the type of reaction in a short string"""
#     return reac.split('_')[-1]
#
#
# # EXAMPLE
# reac_type("Xe_e_ela")

###################################


# def mass_reac(reac):  # TODO change this name. used to check is e- or heavy particle
#     """ Return the mass of the second reactant of the reaction, in kg"""
#     spe = reac.split('_')[1]
#     return mass(spe)

####################################


def mass(part):
    """ Returns the mass of a particle, in kg.

    mass('I2p') = 126.905 * 2 * 1.67E-27
    """

    while part[-1] == 'p' or part[-1] == 'm' or part[-1] == '+' or part[-1] == '-' or part[-1] == '^':  # for I2p or Im I guess.
        part = part[:-1]  # remove last character

    if part == 'e':  # TODO nomenclature précise des espèces, conventions de notations.
        return m_e

    else:

        if str.isdigit(part[-1]):
            number_of_elements = eval(part[-1])
            part = part[:-1]

        else:
            number_of_elements = 1

    # try:
    #     massno = eval(part[-1])
    # except NameError:
    #     massno = 1

        return masses_dictionary[part] * number_of_elements * 1.67e-27

#####


def line_number(reactype, lxfile):
    """Return the line number from which to read the data for a given reaction type."""

    with open(lxfile, 'r') as f:

        reaction_number = eval(reactype[-1]) if reactype[-1].isdigit() else 1

        lines = f.readlines()
        good_line_numbers = []

        for (a, b) in enumerate(lines):
            if b.startswith(reactype):
                good_line_numbers.append(a)
        try:
            return good_line_numbers[reaction_number-1]
        except IndexError:
            print('reaction {} not found'.format(reactype))
        #
        # lineno = 0
        # l = f.readline()
        #
        # if reactype[3:] == '':  # for example, EXC1[3:]=1
        #     reaction_number = 1
        #
        # else:
        #     reaction_number = eval(reactype[3:])
        #
        # reac_count = 0
        #
        # while reac_count != reaction_number or l[:3] != reactype[:3]: # boucle infinie si la ligne n'existe pas.
        #     lineno += 1
        #     l = f.readline()
        #     if l[:3] == reactype[:3]:
        #         reac_count += 1
        #
        # return lineno

#######


def extract_cross_section_table(reactype, lxfile):
    """ Read lxfile and return the relevant table of (Energy, cross section) data."""

    with open( lxfile, 'r') as f:
        content = [x.strip() for x in f.readlines()]

        content = content[line_number(reactype, lxfile):]
        cstab = []

        i = 0
        while content[i][0:7] != '-------':
            i += 1
        i += 1

        while content[i][0:7] != '-------':
            temp_data = content[i].split('\t')
            try:
                cstab.append([eval(temp_data[0].strip()), eval(temp_data[1].strip())])
            except:
                space = '               '
                nspace = 0
                crit = True
                while nspace < len(space) and crit:
                    crit = False
                    try:
                        temp_data = content[i].split(space[nspace:])
                        cstab.append([eval(temp_data[0].strip()), eval(temp_data[1].strip())])
                    except:
                        crit = True
                    nspace += 1
            i += 1

        return np.array(cstab)


def integrate_over_maxwellian(T, m, Ec, c_cs):
    """ Reaction rate at temperature T (en eV) for the cross section data (Ec, cs).

    Integrate the cross sections over a Maxwellian.
    """

    f = np.zeros((len(Ec) - 1, np.size(T)))
    K = np.zeros(np.size(T))

    for i in range(0, len(Ec) - 1):
        f[i, :] = c_cs[i] * np.sqrt(2 * e * Ec[i] / m) * np.exp(-Ec[i] / T) * 4 * pi * 2 * e * Ec[i] / m

    for i in range(1, len(Ec) - 1):
        K += 0.5 * (f[i, :] + f[i - 1, :]) * (Ec[i] - Ec[i - 1]) * np.sqrt(e / (m * (Ec[i] + Ec[i - 1])))

    K *= (m / (2 * pi * e * T)) ** 1.5

    if np.size(T) == 1:
        K = K[0]

    return K


def uB(Te, part):
        """Bohm velocity."""
        return np.sqrt(e * Te / mass(part))


def v_th(Tg, part):
    """Thermal velocity."""
    return np.sqrt((8 * e * Tg) / (pi * mass(part)))


def wpe(n):
    """plasma frequency [rad/s]"""
    return np.sqrt(e**2*n/(epsilon_0*m_e)) 

def l_Debye(n,T):
    """Debye length [m]"""
    return np.sqrt(epsilon_0*T/(e*n))   


def v_Te(T):
    """ Electron 'thermal' velocity """
    return (e*T/m_e)**0.5


def init(text_file):
    """Return a vector of initial densities and temperature"""
    init_vect = []
    lines = relevant_lines(text_file)
    section_line_numbers = [i for i, x in enumerate(lines) if '$$' in x]

    index_species = lines.index('$$ SPECIES $$')
    index_end_species = section_line_numbers[section_line_numbers.index(index_species)+1]

    index_temperatures = lines.index('$$ TEMPERATURES $$')
    index_end_temperatures = section_line_numbers[section_line_numbers.index(index_temperatures)+1]

    irange = np.append(np.arange(index_species+1, index_end_species), np.arange(index_temperatures+1, index_end_temperatures))
    return [eval(lines[i].split('=')[1].strip()) for i in irange]


###################


def lines_in_section(section, text_file):
    """return the list of the lines in a given section"""
    lines = relevant_lines(text_file)
    section_line_numbers = [i for i, x in enumerate(lines) if '$$' in x]

    index_section = lines.index('$$ {} $$'.format(section))  # number of the line where $$ SECTION $$ is.
    index_end_section = section_line_numbers[
                                        section_line_numbers.index(index_section) + 1]  # number of the next section.
    return [lines[i] for i in np.arange(index_section + 1, index_end_section)]
