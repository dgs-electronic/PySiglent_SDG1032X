import visa
import matplotlib
import matplotlib.pyplot as pl
import scipy.signal.windows as win
from numpy import abs, log10
from numpy.fft import fftshift, fftfreq
from scipy.fftpack import fft, next_fast_len
from matplotlib.pyplot import plot, semilogx, grid, loglog, semilogy, figure, xlabel, ylabel, legend, show

class SignalGen:
    def __init__(self, instrument=0):
        self.gen = instrument

    def getidentity(self):
        return self.gen.query("*IDN?")

    def getOutputState(self,channel):
        return self.gen.query("C"+str(channel)+":OUTP?")

    def setOutputState(self,channel,on_off):
        if on_off > 0:
            state = "ON"
        else:
            state = "OFF"
        self.gen.write("C"+str(channel)+":OUTP "+state)
        return "-DONE-"

    def setOutputPolarity(self,channel,polarity):
        if polarity > 0:
            pol = "INVT"
        else:
            pol = "NOR"
        self.gen.write("C"+str(channel)+":OUTP PLRT,"+pol)
        return "-DONE-"

    def setWaveType(self,channel,type):
        wavtyp = {0: "SINE", 1: "SQUARE", 2: "RAMP", 3: "PULSE", 4: "NOISE",
                  5: "ARB", 6: "DC", 7: "PRBS"}
        self.gen.write("C" + str(channel) + ":BSWV WVTP," + wavtyp[type])
        return "-DONE-"

    def setFrequency(self,channel,F):
        self.gen.write("C" + str(channel) + ":BSWV FRQ," + str(F))
        return "-DONE-"

    def setPeriod(self,channel,T):
        self.gen.write("C" + str(channel) + ":BSWV PERI," + str(T))
        return "-DONE-"

    def setAmplitude(self,channel,Amp):
        self.gen.write("C" + str(channel) + ":BSWV AMP," + str(Amp))
        return "-DONE-"

    def setOffset(self,channel,ofst):
        self.gen.write("C" + str(channel) + ":BSWV OFST," + str(ofst))
        return "-DONE-"

    def setSymmetry(self,channel,sym):
        self.setWaveType(channel,2)
        self.gen.write("C" + str(channel) + ":BSWV SYM," + str(sym))
        return "-DONE-"

    def setDuty(self,channel,D):
        self.setWaveType(channel,1)
        self.gen.write("C" + str(channel) + ":BSWV DUTY," + str(D))
        return "-DONE-"

    def setPhase(self,channel,phi):
        self.gen.write("C" + str(channel) + ":BSWV PHSE," + str(phi))
        return "-DONE-"

    def setPulsWidth(self,channel,width):
        self.setWaveType(channel, 3)
        self.gen.write("C" + str(channel) + ":BSWV WIDTH," + str(width))
        return "-DONE-"

    def setPulsRise(self,channel,rise):
        self.setWaveType(channel, 3)
        self.gen.write("C" + str(channel) + ":BSWV RISE," + str(rise))
        return "-DONE-"

    def setPulsFall(self,channel,fall):
        self.setWaveType(channel, 3)
        self.gen.write("C" + str(channel) + ":BSWV FALL," + str(fall))
        return "-DONE-"

    def enableSweep(self,channel):
        self.gen.write("C" + str(channel) + ":SWWV STATE,ON")
        return "-DONE-"

    def disableSweep(self,channel):
        self.gen.write("C" + str(channel) + ":SWWV STATE,OFF")
        return "-DONE-"

    def setSweepTime(self,channel,time):
        self.enableSweep(channel)
        self.gen.write("C" + str(channel) + ":SWWV TIME,"+str(time))
        self.disableSweep(channel)
        return "-DONE-"

    def setSweepStart(self,channel,FStart):
        self.enableSweep(channel)
        self.gen.write("C" + str(channel) + ":SWWV START,"+str(FStart))
        self.disableSweep(channel)
        return "-DONE-"

    def setSweepStop(self,channel,FStop):
        self.enableSweep(channel)
        self.gen.write("C" + str(channel) + ":SWWV STOP,"+str(FStop))
        self.disableSweep(channel)
        return "-DONE-"

    def setSweepMode(self,channel,Mode):
        self.enableSweep(channel)
        if Mode > 0:
            M = "LOG"
        else:
            M = "LINE"
        self.gen.write("C" + str(channel) + ":SWWV SWMD,"+M)
        self.disableSweep(channel)
        return "-DONE-"

    def setSweepDirection(self,channel,Dir):
        self.enableSweep(channel)
        if Dir > 0:
            M = "DOWN"
        else:
            M = "UP"
        self.gen.write("C" + str(channel) + ":SWWV DIR,"+M)
        self.disableSweep(channel)
        return "-DONE-"

    def enableSweepTrigOut(self,channel):
        self.enableSweep(channel)
        self.gen.write("C" + str(channel) + ":SWWV TRSR,INT")
        self.gen.write("C" + str(channel) + ":SWWV TRMD,ON")
        self.disableSweep(channel)
        return "-DONE-"

    def disableSweepTrigOut(self, channel):
        self.enableSweep(channel)
        self.gen.write("C" + str(channel) + ":SWWV TRSR,INT")
        self.gen.write("C" + str(channel) + ":SWWV TRMD,OFF")
        self.disableSweep(channel)
        return "-DONE-"


matplotlib.use('TkAgg')


_rm = visa.ResourceManager()

instrument = _rm.open_resource("TCPIP::192.168.178.68::INSTR")
signal = SignalGen(instrument)
print(signal.getidentity())
#print(signal.setOutputState(1,1))
#print(signal.setOutputPolarity(1,0))
print(signal.setSweepStart(1,1000))
print(signal.setSweepStop(1,5000))
print(signal.setSweepMode(1,0))
print(signal.setSweepDirection(1,1))
signal.disableSweep(1)



instrument.close()