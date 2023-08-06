# from scipy.constants import e, pi, m_e, k
# import numpy as np
# from objects_generator import Reaction
#
# #m_Xe = 131 * 1.66e-27       # Xe mass, kg
# #E_iz_Xe = 12.127            # ev, ionization energy
# #E_exc_Xe = 11.6             # ev, excitation energy
# #kappa = 5.69e-3 * e / k     # Xe gas thermal conductivity
# #sigma_i = 1E-18             # m2, global cross section from Chabert, 2012.
#
# # This works just by chance, but why not?
# for reac in Reaction.reactions_dictionary.keys():
#     sk = 'Reaction.reactions_dictionary["'+reac+'"].K'  # fonction
#     exec('K_'+reac+' = '+sk)
#     se = 'Reaction.reactions_dictionary["'+reac+'"].energy_loss'
#     exec('E_'+reac+' = '+se)
#
#
#
# def K_exc_Xe(Te):  # Te en eV !
#     """Electron impact excitation rate, m3/s-1."""
#     v_mean_e = ((8 * e * Te)/(pi * m_e))**(0.5)
#     return 1.93E-19 * Te**(-0.5) * np.exp(- E_exc_Xe / Te) * v_mean_e
#
#
# def K_iz_Xe(Te):
#     """Electron impact ionization rate, m3/s-1."""
#     v_mean_e = ((8 * e * Te)/(pi * m_e))**(0.5)
#     K_iz1 = 1E-20 * ((3.97 + 0.643*Te - 0.0368 * Te**2) * np.exp(-E_iz_Xe / Te)) * v_mean_e
#     K_iz2 = 1E-20 * (-1.031e-4 * Te**2 + 6.386 * np.exp(-E_iz_Xe/Te)) * v_mean_e
#     return (K_iz1 + K_iz2)/2
#
#
# def K_el_Xe(Te):
#     """Electron impact elastic scattering rate, m3/s-1."""
#     return 3e-13
#
#
# def K_in_Xe(Tg):
#     """Ion neutral elastic collision rate, m3/s-1."""
#     v_mean_ion = np.sqrt((8 * e * Tg)/(pi * m_Xe))
#     return sigma_i * v_mean_ion
#
# def K_Im_I2p_CEX(Te):
#     """ I2^+ - I^- charge exchange, m3/s-1 """
#     return 1.22e-13 # Henry p. 41
#
# def K_Im_Ip_CEX(Te):
#     """ I^+ - I^- ion recombination, m3/s-1 """
#     return 9.311e-15 # Yeung 1957  Tp=Tn et T_ion=T_g
#
#
