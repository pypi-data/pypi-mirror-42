########################################################################
#                                                                      #
#    #######  ########        ## ########  ######  ########  ######    #
#   ##     ## ##     ##       ## ##       ##    ##    ##    ##    ##   #
#   ##     ## ##     ##       ## ##       ##          ##    ##         #
#   ##     ## ########        ## ######   ##          ##     ######    #
#   ##     ## ##     ## ##    ## ##       ##          ##          ##   #
#   ##     ## ##     ## ##    ## ##       ##    ##    ##    ##    ##   #
#    #######  ########   ######  ########  ######     ##     ######    #
#                                                                      #
########################################################################

# This file encompasses the classes objects, thruster, and propellant.

# Written by Florian Marmuse, January 2018

# Requirements for the input text file :
# # is to comment
# $$ shall only appear in section titles
# finish with $$ ENDFILE $$

# Best pratices for the input text file :
# Write e- first in the species.

# TBD: remove the absolute path to files.
# raise a warning is a species in the reaction set is not in species


import numpy as np
from scipy.constants import e, k, pi, m_e
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from toolbox_functions import persecond_to_sccm, all_reactions,  \
    line_number, extract_cross_section_table, mass, integrate_over_maxwellian,\
    reaction_elements,  remove_charge, lines_in_section, get, relevant_lines, \
    wpe, v_Te, uB

# profiler
from cProfile import Profile
from pstats import Stats
import pickle


# TODO Approximation of sigma_i. It should be calculated through sigma_i = K_reac/v_th.
sigma_i = 1.e-18


###############################################################################
#                                                                             #
# ######## ##     ## ########  ##     ##  ######  ######## ######## ########  #
#    ##    ##     ## ##     ## ##     ## ##    ##    ##    ##       ##     ## #
#    ##    ##     ## ##     ## ##     ## ##          ##    ##       ##     ## #
#    ##    ######### ########  ##     ##  ######     ##    ######   ########  #
#    ##    ##     ## ##   ##   ##     ##       ##    ##    ##       ##   ##   #
#    ##    ##     ## ##    ##  ##     ## ##    ##    ##    ##       ##    ##  #
#    ##    ##     ## ##     ##  #######   ######     ##    ######## ##     ## #
#                                                                             #
###############################################################################


class NewThruster:
    def __init__(self, input_txt):
        """"Constructor"""
        self.R               = get('R',             'THRUSTER', input_txt)
        self.L               = get('L',             'THRUSTER', input_txt)
        self.beta_neutrals   = get('beta_neutrals', 'THRUSTER', input_txt)
        self.beta_ions       = get('beta_ions',     'THRUSTER', input_txt)
        self.R_coil          = get('R_coil',        'THRUSTER', input_txt)
        self.w               = get('w',             'THRUSTER', input_txt)
        self.N               = get('N',             'THRUSTER', input_txt)
        self.Vgrids          = get('Vgrids',        'THRUSTER', input_txt)
        self.grid_dist       = get('grid_dist',     'THRUSTER', input_txt)
        self.UQ_coef = 1  # for UQ

    def volume(self):
        """Volume of the thruster."""
        return pi * self.R**2 * self.L

    def total_area(self):
        """Total area of the thruster."""
        return 2 * pi * self.R**2 + 2 * pi * self.R * self.L
	
    def open_area_neutrals(self):
        """Open area of the thruster for the gas."""
        return self.beta_neutrals * pi * self.R**2

    def open_area_ions(self):
        """Open area of the thruster for the ions."""
        return self.beta_ions * pi * self.R**2

    def heat_diff_length(self):
        """Heat diffusion length, from Chabert, 2012."""
        return np.sqrt((self.R / 2.405)**2 + (self.L / pi)**2)

    def hl(self, ng, Te, Tg):
        """Chabert 3.82.
        TODO This is not good. The use of prop/gasname not optimal. Check after we write the prop class.
        """
        
        li = (ng * sigma_i)**(-1)
        betax = 2/pi + 0.1*(0.5 + 0.01*self.L/li)**-1
        return 0.86 * (3 + self.L / (2 * li) + 0.2*(Tg/Te)*(self.L/li)**2)**(-1/2) / betax

    def hr(self, ng):
        """Edge-to-center plasma density ratio.
        TODO Does it makes sense? Can I have different sigma_i for I and I2?
        Answer: Yes, we should have different sigma_i for each ion-atom couple.""" 
        li = (ng * sigma_i)**(-1)
        return 0.8 * (4 + self.R / li)**(-1/2)

    def h0(self, ng, Te, Tg):
        """Global h factor from Romain.
        TODO This is not good. The use of prop/gasname not optimal. Check after we write the prop class.
        """
        effective_area = self.hr(ng) * 2 * pi * self.L * self.R + self.hl(ng, Te, Tg) * 2 * pi * self.R**2
        return self.UQ_coef * (effective_area / self.total_area())

    def h_Bratio(self, ne, ng, Te, Tg, B, mi, Kela):
        """ Ratio between magnetized and non magnetized h factor."""
        alpha = 0.07
        wc    = e*B/m_e
        nue   = Kela*ng
        uB    = (e*Te/mi)**0.5
        nua   = 2*0.6*m_e*wc**2*self.L / (pi**2*mi*uB) # alpha*wc**2/wpe(ne)
        nueff = (nue**2 + nua**2)**0.5
#        nue = nueff
        hB    = v_Te(Te)*(nue+nueff)*(mi/m_e)**0.5/(wc**2 + nue*nueff)/self.L
        G     = self.hl(ng, Te, Tg)/hB
        return ( 1 + G**2 )**-0.5

    def h(self, ne, ng, Te, Tg, B, mi, Kela):
        """Magnetized h factor"""
        return self.hl(ng, Te, Tg)   #*self.h_Bratio(ne, ng, Te, Tg, B, mi, Kela)

    def __str__(self):
        """Readable description of the object, to be called with print."""

        return "The thruster\'s parameters are:\n" \
               "    R = {} m\n" \
               "    L = {} m\n" \
               "    beta_neutrals = {} \n" \
               "    beta_ions = {} \n\n" \
               "For post-processing we use: \n" \
               "    R_coil = {} Ohm\n" \
               "    w = {:.3E} Hz \n" \
               "    Vgrids = {:.2E} V\n" \
               "    Grid distance = {} mm\n\n" \
               "    h at 1E19m-3, 3eV, 300K is {:.2F}".format(self.R, self.L, self.beta_neutrals, self.beta_ions,\
                                                  self.R_coil, self.w / (2*pi), self.Vgrids, self.grid_dist*1000,\
                                                      self.h(1E19, 3, 300))


###################################################################################################
#
# ########     ###    ########     ###    ##     ## ######## ######## ######## ########   ######
# ##     ##   ## ##   ##     ##   ## ##   ###   ### ##          ##    ##       ##     ## ##    ##
# ##     ##  ##   ##  ##     ##  ##   ##  #### #### ##          ##    ##       ##     ## ##
# ########  ##     ## ########  ##     ## ## ### ## ######      ##    ######   ########   ######
# ##        ######### ##   ##   ######### ##     ## ##          ##    ##       ##   ##         ##
# ##        ##     ## ##    ##  ##     ## ##     ## ##          ##    ##       ##    ##  ##    ##
# ##        ##     ## ##     ## ##     ## ##     ## ########    ##    ######## ##     ##  ######
#
###################################################################################################


class NewParameters:
    def __init__(self, input_txt):
        """Constructor."""
        self.B0                 = get('B0',               'PARAMETERS', input_txt) 
        self.Q0                 = get('Q0',               'PARAMETERS', input_txt)
        self.wall_temperature   = get('wall_temperature', 'PARAMETERS', input_txt)
        self.Pabs               = get('Pabs',             'PARAMETERS', input_txt)
        self.stoch_heat         = get('stoch_heat',       'PARAMETERS', input_txt)
        self.Tg                 = get('Tg',               'PARAMETERS', input_txt)
        self.pressure           = get('pressure',         'PARAMETERS', input_txt)
        self.EPS                = get('EPS',              'PARAMETERS', input_txt)

    def __str__(self):
        """Readable description of the object, to be called with print."""
        return "The parameters are: \n" \
               "    Q0 = {} persecond\n" \
               "    Q0 = {} sccm\n" \
               "    Pabs = {} K\n" \
               "    Tg = {} K".format(self.Q0, persecond_to_sccm(self.Q0), self.Pabs, self.Tg)


###############################################################
#
#  ######  ########  ########  ######  #### ########  ######
# ##    ## ##     ## ##       ##    ##  ##  ##       ##    ##
# ##       ##     ## ##       ##        ##  ##       ##
#  ######  ########  ######   ##        ##  ######    ######
#       ## ##        ##       ##        ##  ##             ##
# ##    ## ##        ##       ##    ##  ##  ##       ##    ##
#  ######  ##        ########  ######  #### ########  ######
#
###############################################################


class Species:
    """Contains the species. Contains class attributes, class methods and static methods."""

    number_of_species = 0

    def __init__(self, species_name):
        self.name = species_name
        self.mass = mass(species_name)
        # self.sigma_i =
        # self.kappa =
        Species.number_of_species += 1

    def __str__(self):
        return "Species {} with mass {}.".format(self.name, self.mass)


##################################################################################
#
# ########  ########    ###     ######  ######## ####  #######  ##    ##  ######
# ##     ## ##         ## ##   ##    ##    ##     ##  ##     ## ###   ## ##    ##
# ##     ## ##        ##   ##  ##          ##     ##  ##     ## ####  ## ##
# ########  ######   ##     ## ##          ##     ##  ##     ## ## ## ##  ######
# ##   ##   ##       ######### ##          ##     ##  ##     ## ##  ####       ##
# ##    ##  ##       ##     ## ##    ##    ##     ##  ##     ## ##   ### ##    ##
# ##     ## ######## ##     ##  ######     ##    ####  #######  ##    ##  ######
#
##################################################################################

class Chemistry:
    """Carries R in the parametric analyses."""
    def __init__(self, input_txt):
        self.R = dict()
        self.init_vector = self.make_init_vec(input_txt)

        for line in lines_in_section('REACTIONS', input_txt):
            tmp = Reaction(line)

            try:
                self.R[tmp.reactants[0]][tmp.reactants[1]][tmp.reactype] = tmp
            except KeyError:
                try:
                    self.R[tmp.reactants[0]][tmp.reactants[1]] = dict()
                    self.R[tmp.reactants[0]][tmp.reactants[1]][tmp.reactype] = tmp
                except KeyError:
                    try:
                        self.R[tmp.reactants[0]] = dict()
                        self.R[tmp.reactants[0]][tmp.reactants[1]] = dict()
                        self.R[tmp.reactants[0]][tmp.reactants[1]][tmp.reactype] = tmp
                    except KeyError:
                        print("Init of reaction ", tmp.__str__, "failed.")

    def make_init_vec(self, input_txt):
        init_vec = []

        species_and_init = lines_in_section('SPECIES', input_txt)
        for a in species_and_init:
            init_vec.append(float(a.split('=')[-1]))

        temp_and_init = lines_in_section('TEMPERATURES', input_txt)
        for b in temp_and_init:
            init_vec.append(float(b.split('=')[-1]))

        return init_vec
 

    # def __str__(self):
    #     return str(self.R.items())

class Reaction:
    """Contains a reaction."""
    def __init__(self, line_in_the_reaction_section):

        self.UQ_coef = 1

        self.reaction_elements = reaction_elements(line_in_the_reaction_section)

        self.reactants = self.reaction_elements[0]
        self.products = self.reaction_elements[1]

        self.reactype = self.reaction_elements[2]
        self.rate_given = self.reaction_elements[3]  # False if no rate given

        cwd = os.getcwd()  # current working directory

        self.lxfile = cwd+'/../lxcat/{}_{}.txt'.format(self.reactants[0], self.reactants[1]).replace('e^-', 'e')

        try:
            f = open("{}".format(self.lxfile), 'r')
            f.close()
        except OSError:
            self.lxfile = cwd + '/./lxcat/{}_{}.txt'.format(self.reactants[0], self.reactants[1]).replace('e^-', 'e')

        try:
            with open("{}".format(self.lxfile), 'r') as f:
                content = [x.strip() for x in f.readlines()]
                content = content[line_number(self.reactype, self.lxfile):]

                self.energy_threshold = eval(content[2].strip())  # hardcoded third line

                full_table = extract_cross_section_table(self.reactype, self.lxfile)

                self.energy_table = full_table[:, 0]
                self.cross_section_table = full_table[:, 1]

                if 'e^-' in self.reactants:
                    self.temperature_table = np.linspace(0.05, 30, 250)
                else:
                    self.temperature_table = np.linspace(0.025, 1, 250)

                self.rate_table = integrate_over_maxwellian(self.temperature_table, mass(self.reactants[1]),
                                                            self.energy_table, self.cross_section_table)

        except ValueError:
            self.energy_threshold = 0

        except FileNotFoundError:

            # e.g. when the reaction is not written in the same order than the file..
            if 'e^-' in self.reactants:
                self.temperature_table = np.linspace(0.05, 30, 250)
            else:
                self.temperature_table = np.linspace(0.025, 1, 250) #why was this even there?

            # self.rate_table = self.reactype.split('&')[-1] * np.ones(len(self.temperature_table))


    def __str__(self):
        """Readable description of the object."""
        return "Reaction description:\n" \
               "    {}\n" \
               "    {}\n" \
               "    UQ coef: {}" \
               "    K(3ev): {}".format(self.reaction_elements, self.lxfile, self.UQ_coef, self.K(3))

    def energy_loss(self, dT):
        """Energy loss (eV) of a given reaction, to calculate Ploss. T in eV.
        Corresponds to the energy in line 2 of lxcat columns.
        """

        if self.reactype[:3] == 'ELA':  # elastic
            heavy = self.reactants[0]
            return 3 * dT * (m_e / mass(heavy)) + self.energy_threshold
        else:
            return self.energy_threshold

    def K(self, T):
        """reaction rate, for T in eV."""
        if self.rate_given:  # if not empty
            return self.UQ_coef * self.rate_given
        else:
            return self.UQ_coef * np.interp(T, self.temperature_table, self.rate_table)


########################################################################################
#
#  ######   ######## ##    ## ######## ########     ###    ########  #######  ########
# ##    ##  ##       ###   ## ##       ##     ##   ## ##      ##    ##     ## ##     ##
# ##        ##       ####  ## ##       ##     ##  ##   ##     ##    ##     ## ##     ##
# ##   #### ######   ## ## ## ######   ########  ##     ##    ##    ##     ## ########
# ##    ##  ##       ##  #### ##       ##   ##   #########    ##    ##     ## ##   ##
# ##    ##  ##       ##   ### ##       ##    ##  ##     ##    ##    ##     ## ##    ##
#  ######   ######## ##    ## ######## ##     ## ##     ##    ##     #######  ##     ##
#
#########################################################################################

# def profile(func):
#     def timed_function(*args, **kwargs):
#         pr = Profile()
#         pr.enable()
#         return func(*args, **kwargs)
#         pr.disable()
#         pr.dump_stats('generator_profile_output')
#
#         # with open('profiler_data.pkl', 'wb') as output:
#         #     pickle.dump(Stats('profile_output'), output, pickle.HIGHEST_PROTOCOL)
#
#     return timed_function


# @profile
def generate_all_objects(text_file):
    """Generates thruster, params, and all species and reactions."""
    my_thruster = NewThruster(text_file)
    my_params = NewParameters(text_file)
    my_chem = Chemistry(text_file)

    return my_thruster, my_params, my_chem
