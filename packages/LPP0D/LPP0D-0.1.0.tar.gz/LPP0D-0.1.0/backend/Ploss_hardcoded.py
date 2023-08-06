Ploss = \
    + R['I']['e^-']['EXCITATION'].K(y[6]) * e * R['I']['e^-']['EXCITATION'].energy_loss(y[6] - y[7]) * y[3] * y[0] \
    + R['I2']['e^-']['DISSOCIATIVE_ATTACHMENT'].K(y[6]) * e * R['I2']['e^-']['DISSOCIATIVE_ATTACHMENT'].energy_loss(y[6] - y[7]) * y[2] * y[0] \
    + R['I2']['e^-']['DISSOCIATIVE_IONIZATION'].K(y[6]) * e * R['I2']['e^-']['DISSOCIATIVE_IONIZATION'].energy_loss(y[6] - y[7]) * y[2] * y[0] \
    + R['I']['e^-']['ION'].K(y[6]) * e * R['I']['e^-']['ION'].energy_loss(y[6] - y[7]) * y[3] * y[0] \
    + R['I2']['e^-']['IONIZATION'].K(y[6]) * e * R['I2']['e^-']['IONIZATION'].energy_loss(y[6] - y[7]) * y[2] * y[0] \
    + R['I2']['e^-']['DISSOCIATION'].K(y[6]) * e * R['I2']['e^-']['DISSOCIATION'].energy_loss(y[6] - y[7]) * y[2] * y[0] \
    + 3 * R['I']['e^-']['ELASTIC'].K(y[6]) * e * (y[6] - y[7]) * y[0] * (
                                                                        y[3] * mass('e^-')/mass('I')
                                                                        + y[2] * mass('e^-')/mass('I2')
                                                                        ) \
    + 7 * e * y[6] * (uB(y[6], 'I') * y[4] + uB(y[6], 'I2') * y[5]) * (thruster.hl(ng, y[6], y[7]) * pi * thruster.R**2 + thruster.hr(ng) * 2 * pi * thruster.R * thruster.L) / thruster.volume() \
    + 6 * e * y[6] * (uB(y[6], 'I') * y[4] + uB(y[6], 'I2') * y[5]) * thruster.hl(ng, y[6], y[7]) * thruster.open_area_ions() / thruster.volume()

# + R['I2']['e^-']['ELASTIC'].K(y[6]) * e * R['I2']['e^-']['ELASTIC'].energy_loss(y[6] - y[7]) * y[2] * y[0] \
# + R['I']['e^-']['ELASTIC'].K(y[6]) * e * R['I']['e^-']['ELASTIC'].energy_loss(y[6] - y[7]) * y[3] * y[0] \
#
#  \
# + 2 * e * y[6] * thruster.h(ng, y[6], y[7]) * y[0] * uB(y[6], "I") * d ** (-1) \
#     + 0.5 * e * y[6] * thruster.h(ng, y[6], y[7]) * y[0] * uB(y[6], "I") * d ** (-1) \
#     + 0.5 * np.log(mass("I^+") / (2 * pi * m_e)) * e * y[6] * thruster.h(ng, y[6], y[7]) * y[0] * uB(y[6],
#                                                                                                      "I^+") * d ** (-1) \
#     + 0.5 * np.log(mass("I2^+") / (2 * pi * m_e)) * e * y[6] * thruster.h(ng, y[6], y[7]) * y[0] * uB(y[6],
#                                                                                                       "I2^+") * d ** (-1)