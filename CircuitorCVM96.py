#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
https://pypi.org/project/MinimalModbus/
Descargar usando >> pip install MinimalModbus

Driver para el sensor de estado eléctrico trifásico
Circuitor CVM-NRG96. Implementado sobre la librería
MinimalModbus.

El sensor sólo admite lecturas a su registro y las
distintas funciones get_ implementadas en la clase
CircuitorCVM96 agotan el total de lecturas posibles
según el manual expuesto en la url
http://www.samey.is/_pdf/_circutor/CVM_NRG96_Maelistod_Manual.pdf

Cada función admite dos valores para el keyword "cual"
que son "min" y "max", con los cuales se pide que la
lectura devuelta no sea la actual sino la mínima o la
máxima registradas. Además algunas funciones permiten
alternar entre las líneas L1, L2 y L3 dándole valores
1, 2 y 3 al keyword "L".

Por ejemplo, la funcion get_Current(L=2, cual='max')
devuelve el valor máximo registrado de corriente
de la línea L2.

Lista de funciones get_ implementadas:
  get_Voltage_Phase     \
  get_Current           |
  get_Active_Power      |   All of these admit
  get_Reactive_Power    >   L keyword for the
  get_Power_Factor      |   3 different lines
  get_percent_THD_V     |
  get_percent_THD_A     /
  get_Frecuency
  get_Active_power_III
  get_Inductive_power_III
  get_Capacitive_power_III
  get_Cos_Phi
  get_Power_Factor_III
  get_Voltage_Line_L1_L2
  get_Voltage_Line_L2_L3
  get_Voltage_Line_L3_L1
  get_Apparent_Power_III
  get_Maximum_Demand
  get_Three_Phase_Current
  get_Neutral_Current
  get_Maximum_Demand_A2
  get_Maximum_Demand_A3
  get_Active_Energy
  get_Inductive_Reactive_Energy
  get_Reactive_Energy_Capacitive
  get_Apparent_Energy
  get_Active_Energy_Generated
  get_Inductive_Energy_Generated
  get_Capacitive_Energy_Generated
  get_Apparent_Energy_Generated

'''

import minimalmodbus


class CircuitorCVM96(minimalmodbus.Instrument):
    def read_register(self, reg, decimals=0):
        """ fue preciso sobreescribir esta funcion
        para no cambiar la libreria entera. La funcion
        read_register() de minimalmodbus pide leer un
        solo registro por vez. Para leer el Circuitor
        se precisan pedir dos registros o una cantidad
        par. Para hacer eso la funcion adecuada es
        read_registers()"""
        inp = self.read_registers(reg, numberOfRegisters=2)
        from time import sleep
        # sleep(0.1)
        return (inp[1] + inp[0] * 2 ** 16) / 10. ** decimals

    def __init__(self, port_name, slave_address, baud_rate=9600, timeout=1):
        minimalmodbus.BAUDRATE = baud_rate
        minimalmodbus.TIMEOUT = timeout

        super().__init__(port_name, slave_address)

        self.FuncionesPorLinea = (self.get_Voltage_Phase,
                                  self.get_Current,
                                  self.get_Active_Power,
                                  self.get_Reactive_Power,
                                  self.get_Power_Factor,
                                  self.get_percent_THD_V,
                                  self.get_percent_THD_A)
        self.TitulosDeFuncionesPorLinea = (
            'Tension de Linea',
            'Corriente',
            'Potencia Activa',
            'Potencia Reactiva',
            'Factor de Potencia',
            'Porcentaje de Distorsion Total por Armonicos en Tension',
            'Porcentaje de Distorsion Total por Armonicos en Corriente')
        self.FuncionesTrifasicas = (self.get_Frecuency,
                                    self.get_Active_power_III,
                                    self.get_Inductive_power_III,
                                    self.get_Capacitive_power_III,
                                    self.get_Cos_Phi,
                                    self.get_Power_Factor_III,
                                    self.get_Voltage_Line_L1_L2,
                                    self.get_Voltage_Line_L2_L3,
                                    self.get_Voltage_Line_L3_L1,
                                    self.get_Apparent_Power_III,
                                    self.get_Maximum_Demand,
                                    self.get_Three_Phase_Current,
                                    self.get_Neutral_Current,
                                    self.get_Maximum_Demand_A2,
                                    self.get_Maximum_Demand_A3,
                                    self.get_Active_Energy,
                                    self.get_Inductive_Reactive_Energy,
                                    self.get_Reactive_Energy_Capacitive,
                                    self.get_Apparent_Energy,
                                    self.get_Active_Energy_Generated,
                                    self.get_Inductive_Energy_Generated,
                                    self.get_Capacitive_Energy_Generated,
                                    self.get_Apparent_Energy_Generated)
        self.TitulosDeFuncionesTrifasicas = (
            'Frecuencia',
            'Potencia Activa III',
            'Potencia Inductiva III',
            'Potencia Capacitiva III',
            'Coseno Fi',
            'Factor de Potencia III',
            'Tension entre Lineas L1 y L2',
            'Tension entre Lineas L2 y L3',
            'Tension entre Lineas L3 y L1',
            'Potencia Aparente III',
            'Demanda Maxima',
            'Corriente de las Tres Fases',
            'Corriente de Neutro',
            'Demanda Maxima A2',
            'Demanda Maxima A3',
            'Energia Activa',
            'Energia Reactiva Inductiva',
            'Energia Reactiva Capacitiva',
            'Energia Aparente',
            'Energia Activa Generada',
            'Energia Inductiva Generada',
            'Energia Capacitiva Generada',
            'Energia Aparente Generada')

    def get_Voltage_Phase(self, L=1, cual='instant'):
        # Devuelve la fase de voltaje de L en Volts
        addr = 0x60 if cual == 'max' else 0xc0 if cual == 'min' else 0x00
        shift = 20 if L == 3 else 10 if L == 2 else 0
        return self.read_register(int(addr) + shift, 1)

    def get_Current(self, L=1, cual='instant'):
        # Devuelve la corriente de L en mA
        addr = 0x62 if cual == 'max' else 0xc2 if cual == 'min' else 0x02
        shift = 20 if L == 3 else 10 if L == 2 else 0
        return self.read_register(int(addr) + shift, 0)

    def get_Active_Power(self, L=1, cual='instant'):
        # Devuelve la potencia activa de L en kW
        addr = 0x64 if cual == 'max' else 0xc4 if cual == 'min' else 0x04
        shift = 20 if L == 3 else 10 if L == 2 else 0
        return self.read_register(int(addr) + shift, 0)

    def get_Reactive_Power(self, L=1, cual='instant'):
        # Devuelve la potencia reactiva de L en kvar
        addr = 0x66 if cual == 'max' else 0xc6 if cual == 'min' else 0x06
        shift = 20 if L == 3 else 10 if L == 2 else 0
        return self.read_register(int(addr) + shift, 0)

    def get_Power_Factor(self, L=1, cual='instant'):
        # Devuelve el factor de potencia de L
        addr = 0x68 if cual == 'max' else 0xc8 if cual == 'min' else 0x08
        shift = 20 if L == 3 else 10 if L == 2 else 0
        return self.read_register(int(addr) + shift, 2)

    def get_Frecuency(self, cual='instant'):
        # Devuelve la frecuencia en Hz
        addr = 0x88 if cual == 'max' else 0xe8 if cual == 'min' else 0x28
        return self.read_register(int(addr), 1)

    def get_Active_power_III(self, cual='instant'):
        # kW
        addr = 0x7e if cual == 'max' else 0xde if cual == 'min' else 0x1e
        return self.read_register(int(addr), 0)

    def get_Inductive_power_III(self, cual='instant'):
        # kvarL
        addr = 0x80 if cual == 'max' else 0xe0 if cual == 'min' else 0x20
        return self.read_register(int(addr), 0)

    def get_Capacitive_power_III(self, cual='instant'):
        # kvarC
        addr = 0x82 if cual == 'max' else 0xe2 if cual == 'min' else 0x22
        return self.read_register(int(addr), 0)

    def get_Cos_Phi(self, cual='instant'):
        # Devuelve el coseno Fi
        addr = 0x84 if cual == 'max' else 0xe4 if cual == 'min' else 0x24
        return self.read_register(int(addr), 2)

    def get_Power_Factor_III(self, cual='instant'):
        #
        addr = 0x86 if cual == 'max' else 0xe6 if cual == 'min' else 0x26
        return self.read_register(int(addr), 2)

    def get_Voltage_Line_L1_L2(self, cual='instant'):
        # Devuelve la tension entre L1 y L2 en Volts
        addr = 0x8a if cual == 'max' else 0xea if cual == 'min' else 0x2a
        return self.read_register(int(addr), 1)

    def get_Voltage_Line_L2_L3(self, cual='instant'):
        # Devuelve la tension entre L2 y L3 en Volts
        addr = 0x8c if cual == 'max' else 0xec if cual == 'min' else 0x2c
        return self.read_register(int(addr), 1)

    def get_Voltage_Line_L3_L1(self, cual='instant'):
        # Devuelve la tension entre L3 y L1 en Volts
        addr = 0x8e if cual == 'max' else 0xee if cual == 'min' else 0x2e
        return self.read_register(int(addr), 1)

    def get_percent_THD_V(self, L=1, cual='instant'):
        # Devuelve % de Distorsión Armonica Total de tension de L
        addr = 0x90 if cual == 'max' else 0xf0 if cual == 'min' else 0x30
        shift = 4 if L == 3 else 2 if L == 2 else 0
        return self.read_register(int(addr) + shift, 1)

    def get_percent_THD_A(self, L=1, cual='instant'):
        # Devuelve % de Distorsión Armonica Total de correinte de L
        addr = 0x96 if cual == 'max' else 0xf6 if cual == 'min' else 0x36
        shift = 4 if L == 3 else 2 if L == 2 else 0
        return self.read_register(int(addr) + shift, 1)

    def get_Apparent_Power_III(self, cual='instant'):
        # Devuelve la potencia aparente en kva
        addr = 0xa2 if cual == 'max' else 0x102 if cual == 'min' else 0x42
        return self.read_register(int(addr), 0)

    def get_Maximum_Demand(self, cual='instant'):
        # Devuelve la demanda maxima en kW/VA/mA
        addr = 0xa4 if cual == 'max' else 0x104 if cual == 'min' else 0x44
        return self.read_register(int(addr), 0)

    def get_Three_Phase_Current(self, cual='instant'):
        # Devuelve el promedio de la Corriente de las 3 fases en mA
        addr = 0xa6 if cual == 'max' else 0x106 if cual == 'min' else 0x46
        return self.read_register(int(addr), 0)

    def get_Neutral_Current(self, cual='instant'):
        # mA
        addr = 0xa8 if cual == 'max' else 0x108 if cual == 'min' else 0x48
        return self.read_register(int(addr), 0)

    def get_Maximum_Demand_A2(self, cual='instant'):
        # mA
        addr = 0xb2 if cual == 'max' else 0x112 if cual == 'min' else 0x52
        return self.read_register(int(addr), 0)

    def get_Maximum_Demand_A3(self, cual='instant'):
        # mA
        addr = 0xb4 if cual == 'max' else 0x114 if cual == 'min' else 0x54
        return self.read_register(int(addr), 0)

    def get_Active_Energy(self, cual='instant'):
        # kW-h III
        addr = 0x9c if cual == 'max' else 0xfc if cual == 'min' else 0x3c
        return self.read_register(int(addr), 0)

    def get_Inductive_Reactive_Energy(self, cual='instant'):
        # kvarL-h III
        addr = 0x9e if cual == 'max' else 0xfe if cual == 'min' else 0x3e
        return self.read_register(int(addr), 0)

    def get_Reactive_Energy_Capacitive(self, cual='instant'):
        # kvarC-h III
        addr = 0xa0 if cual == 'max' else 0x100 if cual == 'min' else 0x40
        return self.read_register(int(addr), 0)

    def get_Apparent_Energy(self, cual='instant'):
        # kVA-h III
        addr = 0xb6 if cual == 'max' else 0x116 if cual == 'min' else 0x56
        return self.read_register(int(addr), 0)

    def get_Active_Energy_Generated(self, cual='instant'):
        # kW-h III
        addr = 0xb8 if cual == 'max' else 0x118 if cual == 'min' else 0x58
        return self.read_register(int(addr), 0)

    def get_Inductive_Energy_Generated(self, cual='instant'):
        # kvarL-h III
        addr = 0xba if cual == 'max' else 0x11a if cual == 'min' else 0x5a
        return self.read_register(int(addr), 0)

    def get_Capacitive_Energy_Generated(self, cual='instant'):
        # kvarC-h III
        addr = 0xbc if cual == 'max' else 0x11c if cual == 'min' else 0x5c
        return self.read_register(int(addr), 0)

    def get_Apparent_Energy_Generated(self, cual='instant'):
        # kVA-h III
        addr = 0xbe if cual == 'max' else 0x11e if cual == 'min' else 0x5e
        return self.read_register(int(addr), 0)
