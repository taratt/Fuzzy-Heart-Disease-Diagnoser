"""
@author: Tara Saba
"""
import numpy as np
import math

class FuzzyController:

    def getSets(self, theClass):
        method_list = []
        for attribute in dir(theClass):
            attribute_value = getattr(theClass, attribute)
            if callable(attribute_value):
                if attribute.startswith('__') == False:
                    method_list.append(attribute)
        return method_list

    def get_memberships(self, input, argument):
        method_list = self.getSets(argument.__class__)
        member_dic = {}
        for i in method_list:
            member_dic[i] = getattr(argument.__class__, i)(argument, input)
        return member_dic

    def fuzzify(self, input):
        fuzzified_input = {}
        bl_fuzzi = self.Blood_Fuzzifier()
        fuzzified_input['bl'] = self.get_memberships(input['bl'], bl_fuzzi)

        ch_fuzzi = self.Cholesterol_Fuzzifier()
        fuzzified_input['ch'] = self.get_memberships(input['ch'], ch_fuzzi)

        age_fuzzi = self.Age_Fuzzifier()
        fuzzified_input['age'] = self.get_memberships(input['age'], age_fuzzi)

        max_heart_fuzzi = self.Max_heart_rate_Fuzzifier()
        fuzzified_input['max_heart'] = self.get_memberships(input['max_heart'], max_heart_fuzzi)

        bl_sugar_fuzzi = self.Blood_sugar_Fuzzifier()
        fuzzified_input['sugar'] = self.get_memberships(input['sugar'], bl_sugar_fuzzi)

        pain_fuzzi = self.Chest_pain_Fuzzifier()
        fuzzified_input['pain'] = self.get_memberships(input['pain'], pain_fuzzi)

        gender_fuzzi = self.Gender_Fuzzifier()
        fuzzified_input['gender'] = self.get_memberships(input['gender'], gender_fuzzi)

        old_fuzzi = self.Old_peak_Fuzzifier()
        fuzzified_input['peak'] = self.get_memberships(input['peak'], old_fuzzi)

        return fuzzified_input

    def infer(self, fuzzified_input):
        inferer = self.Rules()
        inferences = inferer.infer(fuzzified_input)
        return inferences

    def calculate_disease_membership(self, x, infered_values):
        disease = self.Disease_presence(infered_values)
        disease_memberships = self.get_memberships(x, disease)
        x_membership = max(disease_memberships.values())
        return x_membership

    def center_of_gravity(self, infered_values):
        force_points = np.linspace(0, 4, 4000)
        dx = force_points[1] - force_points[0]
        integral = 0
        denominator = 0
        for point in force_points:
            u = self.calculate_disease_membership(point, infered_values)
            integral += u * point * dx
            denominator += u * dx
        if denominator == 0:
            return 0

        return float(integral / denominator)

    def decide(self, info):
        fuzzified_input = self.fuzzify(info)

        infered = self.infer(fuzzified_input)
        disease = self.center_of_gravity(infered)
        return round(disease,2)

    class Blood_Fuzzifier:
        def __init__(self):
            pass

        def low(self, x):
            if x < 111:
                return 1
            if 111 <= x < 134:
                return (134 - x) / 23
            return 0

        def medium(self, x):
            if 127 <= x < 139:
                return (x - 127) / 12
            if 139 <= x <= 153:
                return (153 - x) / 14
            return 0

        def high(self, x):
            if 142 <= x < 157:
                return (x - 142) / 15
            if 157 <= x <= 172:
                return (172 - x) / 15
            return 0

        def very_high(self, x):
            if 154 <= x < 171:
                return (x - 154) / 17
            if 171 <= x:
                return 1
            return 0

    class Cholesterol_Fuzzifier:
        def __init__(self):
            pass

        def low(self, x):
            if x < 151:
                return 1
            if 151 <= x < 197:
                return (197 - x) / 46
            return 0

        def medium(self, x):
            if 188 <= x < 215:
                return (x - 188) / 27
            if 215 <= x <= 250:
                return (250 - x) / 35
            return 0

        def high(self, x):
            if 217 <= x < 263:
                return (x - 217) / 46
            if 263 <= x <= 307:
                return (307 - x) / 44
            return 0

        def very_high(self, x):
            if 281 <= x < 347:
                return (x - 281) / 66
            if 347 <= x:
                return 1
            return 0

    class Age_Fuzzifier:
        def __init__(self):
            pass

        def young(self, x):
            if x < 29:
                return 1
            if 29 <= x < 38:
                return (38 - x) / 9
            return 0

        def mild(self, x):
            if 33 <= x < 38:
                return (x - 33) / 5
            if 38 <= x <= 45:
                return (45 - x) / 7
            return 0

        def old(self, x):
            if 40 <= x < 48:
                return (x - 40) / 8
            if 48 <= x <= 58:
                return (58 - x) / 10
            return 0

        def very_old(self, x):
            if 52 <= x < 60:
                return (x - 52) / 8
            if 60 <= x:
                return 1
            return 0
    class Old_peak_Fuzzifier:
        def __init__(self):
            pass

        def low(self, x):
            if x < 1:
                return 1
            if 1 <= x < 2:
                return 2 - x
            return 0

        def risk(self, x):
            if 1.5 <= x < 2.8:
                return (x - 1.5) / 1.3
            if 2.8 <= x <= 4.2:
                return (4.2 - x) / 1.4
            return 0

        def terrible(self, x):
            if 2.55 <= x < 4:
                return (x - 2.55) / 1.45
            if 4 <= x :
                return 1
            return 0

    class Max_heart_rate_Fuzzifier:
        def __init__(self):
            pass

        def low(self, x):
            if x < 100:
                return 1
            if 100 <= x < 141:
                return (141 - x) / 41
            return 0

        def medium(self, x):
            if 111 <= x < 152:
                return (x - 111) / 41
            if 152 <= x <= 194:
                return (194 - x) / 42
            return 0

        def high(self, x):
            if 152 <= x < 216:
                return (x - 152) / 64
            if x >= 216:
                return 1
            return 0

    class Blood_sugar_Fuzzifier:
        def __init__(self):
            pass

        def very_high(self, x):
            if 105 <= x < 120:
                return (x - 105) / 15
            if x >= 120:
                return 1
            return 0

    class Chest_pain_Fuzzifier:
        def __init__(self):
            pass

        def ty_ang(self, x):
            if x == 1:
                return 1
            return 0

        def aty_ang(self, x):
            if x == 2:
                return 1
            return 0

        def non_ang(self, x):
            if x == 3:
                return 1
            return 0

        def asym(self, x):
            if x == 4:
                return 1
            return 0

    class Gender_Fuzzifier:
        def __init__(self):
            pass

        def male(self, x):
            if x == 0:
                return 1
            return 0

        def female(self, x):
            if x == 1:
                return 1
            return 0

    class Disease_presence:
        def __init__(self, infered_values):
            self.infered_values = infered_values

        def healthy(self, x):
            membership = 0
            if x < 0.78:
                membership = 1
            if 0.78 <= x <= 1.78:
                membership = (1.78 - x)
            return min(membership, self.infered_values['healthy'])

        def s1(self, x):
            membership = 0
            if 1 <= x < 1.75:
                membership = (x-1) / 0.75
            if 1.75 <= x <= 2.51:
                membership = (2.51 - x) /0.76
            return min(membership, self.infered_values['s1'])

        def s2(self, x):
            membership = 0
            if 1.78 <= x < 2.5:
                membership = (x-1.78) / 0.72
            if 2.5 <= x <= 3.25:
                membership = (3.25 - x) /0.75
            return min(membership, self.infered_values['s2'])

        def s3(self, x):
            membership = 0
            if 2.5 <= x < 3.5:
                membership = (x - 2.5)
            if 3.5 <= x <= 4.5:
                membership = (4.5 - x)
            return min(membership, self.infered_values['s3'])

        def s4(self, x):
            membership = 0
            if 3.25 <= x < 3.75:
                membership = (x - 3) / 0.75
            if 3.75 <= x:
                membership = 1
            return min(membership, self.infered_values['s4'])



    class Rules:
        def __init__(self):
            pass

        def infer(self, input):
            blood_pressure = input['bl']
            ch = input['ch']
            age = input['age']
            max_heart = input['max_heart']
            sugar = input['sugar']
            pain = input['pain']
            gender = input['gender']
            peak = input['peak']
            disease_presence = {}
            dis_terms = ['healthy', 's1', 's2', 's3', 's4']
            for dis in dis_terms:
                disease_presence[dis] = 0

            disease_presence['healthy'] = max(pain['ty_ang'], disease_presence['healthy'])
            disease_presence['s1'] = max(pain['aty_ang'], disease_presence['s1'])
            disease_presence['s2'] = max(pain['non_ang'], disease_presence['s2'])
            disease_presence['s3'] = max(pain['asym'], disease_presence['s3'])
            disease_presence['s4'] = max(pain['asym'], disease_presence['s4'])

            disease_presence['s1'] = max(gender['female'], disease_presence['s1'])
            disease_presence['s2'] = max(gender['male'], disease_presence['s2'])

            disease_presence['healthy'] = max(blood_pressure['low'], disease_presence['healthy'])
            disease_presence['s1'] = max(blood_pressure['medium'], disease_presence['s1'])
            disease_presence['s2'] = max(blood_pressure['high'], disease_presence['s2'])
            disease_presence['s3'] = max(blood_pressure['high'], disease_presence['s3'])
            disease_presence['s4'] = max(blood_pressure['very_high'], disease_presence['s4'])

            disease_presence['healthy'] = max(ch['low'], disease_presence['healthy'])
            disease_presence['s1'] = max(ch['medium'], disease_presence['s1'])
            disease_presence['s2'] = max(ch['high'], disease_presence['s2'])
            disease_presence['s3'] = max(ch['high'], disease_presence['s3'])
            disease_presence['s4'] = max(ch['very_high'], disease_presence['s4'])

            disease_presence['s2'] = max(sugar['very_high'], disease_presence['s2'])

            disease_presence['healthy'] = max(max_heart['low'], disease_presence['healthy'])
            disease_presence['s1'] = max(max_heart['medium'], disease_presence['s1'])
            disease_presence['s2'] = max(max_heart['medium'], disease_presence['s2'])
            disease_presence['s3'] = max(max_heart['high'], disease_presence['s3'])
            disease_presence['s4'] = max(max_heart['high'], disease_presence['s4'])

            disease_presence['healthy'] = max(age['young'], disease_presence['healthy'])
            disease_presence['s1'] = max(age['mild'], disease_presence['s1'])
            disease_presence['s2'] = max(age['old'], disease_presence['s2'])
            disease_presence['s3'] = max(age['old'], disease_presence['s3'])
            disease_presence['s4'] = max(age['very_old'], disease_presence['s4'])

            disease_presence['healthy'] = max(peak['low'], disease_presence['healthy'])
            disease_presence['s1'] = max(peak['low'], disease_presence['s1'])
            disease_presence['s2'] = max(peak['terrible'], disease_presence['s2'])
            disease_presence['s3'] = max(peak['terrible'], disease_presence['s3'])
            disease_presence['s4'] = max(peak['risk'], disease_presence['s4'])


            return disease_presence

def main():
    controller = FuzzyController()
    info = {}
    info['pain'] = int(input("Chest pain: "))
    info['bl'] = int(input("Blood pressure: "))
    info['ch'] = int(input("Cholesterol: "))
    info['sugar'] = int(input("Blood sugar: "))
    info['max_heart'] = int(input("Maximum heart rate: "))
    info['age'] = int(input("Age: "))
    info['gender'] = int(input("Gender: "))
    info['peak'] = float(input("Old peak: "))
    disease_presence = controller.decide(info)
    print("*******")
    print("Results on scale one to four: "+ str(disease_presence))
    if math.floor(disease_presence)==0:
        status = "Status: Healthy"
    else:
        status = "Heart Sickness Presence Level: s"+str(round(disease_presence))
    print(status)

if __name__ == '__main__':
    main()