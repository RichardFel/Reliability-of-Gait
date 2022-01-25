import numpy as np
import Visualise
   
def rotateToGlobal(leftfoot, rightfoot, plotje):
    rightfoot = fuse(rightfoot, plotje)
    leftfoot = fuse(leftfoot, plotje)
    return {'leftfoot': leftfoot, 'rightfoot' : rightfoot}

def fuse(self, plotje):
    self.fusion = sensorFusion()
    sensorFusion.linearAcceleration(self, plotje = plotje)
    sensorFusion.VelocityPosition(self, veldriftcorrection = True)
    return self 

def qMult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = (w1 * w2) - (x1 * x2) - (y1 * y2) - (z1 * z2)
    x = (w1 * x2) + (x1 * w2) + (y1 * z2) - (z1 * y2)
    y = (w1 * y2) - (x1 * z2) + (y1 * w2) + (z1 * x2)
    z = (w1 * z2) + (x1 * y2) - (y1 * x2) + (z1 * w2)
    return w, x, y, z

def qConjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def qvMult(v1, q1):
    v0xyz = qMult(qMult(q1,v1), qConjugate(q1))
    return [v0xyz[1],v0xyz[2],v0xyz[3]]
 
class sensorFusion:
    def __init__(self):
            self.q = [1,0,0,0]                              
            self.kpinit = 200                              
            self.initperiod = 5                             
            self.interror= np.array([0.0, 0.0, 0.0])         
            self.sampleperiod = 0.01
            self.kpramped = self.ki = 0 
            self.beta = 1
            
    def linearAcceleration(self, plotje = None):
        sensorFusion.initQuaternion(self)
        sensorFusion.stationairy(self)
        sensorFusion.globalAcceleration(self)
        if plotje:
            Visualise.plot1(self.linearacc, title = 'Corrected acceleration signals AP, ML, VT'
                             , xlabel = 'Samples', ylabel = 'Acceleration [m/s^2]')

    def initQuaternion(self):
        accconv = self.acceleration[0:self.walkPart[0]]
        if (len(accconv) > 100):                                     
            for _ in range(len(accconv)):                                            
                self.fusion.update_6dof([np.mean(accconv[:,0]), 
                                         np.mean(accconv[:,1]), 
                                         np.mean(accconv[:,2])],[0,0,0], kp= 1)
    
    def stationairy(self):
        self.stationary = np.array([])
        for sample in self.standphases:
            self.stationary = np.concatenate((self.stationary,sample))

    def globalAcceleration(self):
        self.quaternion = np.zeros((len(self.acceleration),4))
        self.linearacc = np.zeros((len(self.acceleration),3))
        self.gyrRotated = np.zeros((len(self.gyroscope),3))
        for sample in range(len(self.acceleration)):                                        
            if sample in self.stationary:
                self.quaternion[sample] = self.fusion.update_6dof(np.array(self.acceleration)[sample], 
                np.array(self.gyroscope)[sample], kp = 0.5)
            else:
                self.quaternion[sample] = self.fusion.update_6dof(np.array(self.acceleration)[sample], 
                np.array(self.gyroscope)[sample], kp = 0)
            self.linearacc[sample] = self.fusion.linearacc(self.acceleration[sample], self.quaternion[sample])
            self.gyrRotated[sample] = self.fusion.linearacc(self.gyroscope[sample], self.quaternion[sample])
        self.linearacc *= 9.81
        self.linearacc[:,2] -= 9.81
        self.accRotated = self.linearacc
        
    def update_6dof(self,acceleration, gyroscope, kp):   
        acceleration /=  np.linalg.norm(acceleration)
        v = np.array([2*(self.q[1]*self.q[3] - self.q[0]*self.q[2]), 
                      2*(self.q[0]*self.q[1] + self.q[2]*self.q[3]), 
                      self.q[0]**2 - self.q[1]**2 - self.q[2]**2 + self.q[3]**2]);               	
        error = np.array(np.cross(v, acceleration))
        
        if self.kpramped > kp:
            self.interror = np.array([0.0, 0.0, 0.0])
            self.kpramped -= ( (self.kpinit - kp) / (self.initperiod / self.sampleperiod))
        else: 
            self.kpramped = kp
            self.interror += error
        ref = gyroscope - (kp*error + self.ki*self.interror)                
        qDot1 = 0.5 * np.array(qMult(tuple(self.q), (0.0, ref[0],ref[1],ref[2])))
        self.q = self.q + qDot1 * self.sampleperiod
        self.q /= np.linalg.norm(self.q)
        return qConjugate(self.q)

    def VelocityPosition(self,veldriftcorrection = True):
        self.velocity = self.fusion.velocity(self.linearacc, self.stationary)                 
        if veldriftcorrection:
            veldrift = np.zeros((len(self.velocity),3))
            for count, value in enumerate(self.standphases[1:-1]):
                driftrate = self.velocity[value[0]-1] / (value[0] - self.standphases[count][-1])
                enum = np.arange(value[0] - self.standphases[count][-1])
                drift = np.transpose(np.array((enum,enum,enum))) * driftrate
                veldrift[self.standphases[count][-1]:value[0]] = drift
            self.velocity -= veldrift
        self.position = self.fusion.position(self.velocity)     
     
    def linearacc(self, acceleration, quaternion):
        v1 = (0.0, acceleration[0], acceleration[1], acceleration[2])
        q1 = qConjugate(quaternion)
        return qvMult(v1, q1)
    
    def velocity(self, linearacc, stationary):
        vel = np.zeros((len(linearacc),3))
        for i in range(1, len(vel)):
            j = i - 1
            vel[i] = vel[j] + linearacc[i] * self.sampleperiod
            if (i in stationary) :
                vel[i] = 0
        return vel
        
    def position(self, vel):
        pos = np.zeros((len(vel),3))
        for i in range(1, len(pos)):
            j = i - 1
            pos[i] = pos[j] + vel[i] * self.sampleperiod 
        return pos
       
    def caclrot(self, order):
        '''
        Calculate the orientation of the sensor in a global axis. 
        '''

        #    order = 'yzx'
        #    
        #    def caclrot(q, order):
        #        from scipy.spatial.transform import Rotation as R
        #        r = R.from_quat([q[0], q[1], q[2], q[3]])
        #        ang = r.as_euler(order, degrees=True)
        #        return ang
        #    
        #    import numpy as np
        #    
        #    angles = np.zeros((len(sensors["rightfoot"].quaternion),3))
        #    for i in range(0,len(angles)):
        #        angles[i] = caclrot(sensors["rightfoot"].quaternion[i],order)
        #
        #    # Set baseline at 0
        #    angles -= np.mean(angles[0:200,:], axis = 0)
        #
        #    import matplotlib.pyplot as plt
        #    signal = angles
        #    fig1, ax2 = plt.subplots(3)
        #    ax2[0].plot(np.array(range(0,len(signal))),signal[:,0])
        #    ax2[1].plot(np.array(range(0,len(signal))), signal[:,1])
        #    ax2[2].plot(np.array(range(0,len(signal))), signal[:,2])  
        
        from scipy.spatial.transform import Rotation as R
        r = R.from_quat([self.quaternion[0], self.quaternion[1], self.quaternion[2], self.quaternion[3]])
        ang = r.as_euler(order, degrees=True)
        
        return ang
    