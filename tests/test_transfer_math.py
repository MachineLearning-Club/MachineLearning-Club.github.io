"""Numerical regression checks for the Week 1–7 conceptual bridges."""
from collections import Counter
from math import log2, exp
import unittest

def entropy(labels):
    c=Counter(labels);n=len(labels)
    return -sum((v/n)*log2(v/n) for v in c.values()) if n else 0.0

class TransferMathTests(unittest.TestCase):
    def test_conditional_probability(self):
        die=list(range(1,11))
        self.assertEqual(sum(x==2 for x in die if x%2==0),1)
        self.assertEqual(len([x for x in die if x%2==0]),5)

    def test_id3_global_and_conditional_gain(self):
        # This reproduces the twelve-row fictional diary of Week 2.
        rows=[('sunny','calm','yes')]*2+[('sunny','windy','yes')]*2
        rows += [('cloudy','calm','yes')]*2+[('cloudy','windy','no')]*2
        rows += [('rainy','calm','no')]*2+[('rainy','windy','no')]*2
        labels=[r[2] for r in rows]
        groups={sky:[r[2] for r in rows if r[0]==sky] for sky in ('sunny','cloudy','rainy')}
        gain=entropy(labels)-sum(len(g)/len(labels)*entropy(g) for g in groups.values())
        self.assertAlmostEqual(gain,2/3)
        cloudy=[r for r in rows if r[0]=='cloudy']
        wind_groups=[[r[2] for r in cloudy if r[1]==value] for value in ('calm','windy')]
        conditional=entropy([r[2] for r in cloudy])-sum(len(g)/4*entropy(g) for g in wind_groups)
        self.assertAlmostEqual(conditional,1.0)

    def test_kmeans_centroids_and_objective(self):
        group1=[(-1,0),(1,0),(0,1)]
        group2=[(3,0),(3,1)]
        mean=lambda group:tuple(sum(p[i] for p in group)/len(group) for i in (0,1))
        a,b=mean(group1),mean(group2)
        sq=lambda p,c:sum((x-y)**2 for x,y in zip(p,c))
        objective=sum(sq(p,a) for p in group1)+sum(sq(p,b) for p in group2)
        self.assertEqual(a,(0,1/3))
        self.assertEqual(b,(3,.5))
        self.assertAlmostEqual(objective,19/6)
        self.assertAlmostEqual(sum(sq(p,group1[0]) for p in group1)+
                               sum(sq(p,group2[-1]) for p in group2),7)

    def test_confusion_metrics(self):
        tp,tn,fp,fn=2,2,1,1
        self.assertEqual((tp+tn)/(tp+tn+fp+fn),4/6)
        self.assertEqual(tp/(tp+fp),2/3)
        self.assertEqual(tp/(tp+fn),2/3)

    def test_image_threshold_boundary(self):
        numbers=[30,100,127,128,220,255]
        self.assertEqual([0 if v<128 else 255 for v in numbers],[0,0,0,255,255,255])

    def test_perceptron_and_xor(self):
        inputs=[(0,0),(0,1),(1,0),(1,1)]
        and_pred=[int(x+y-1.5>=0) for x,y in inputs]
        xor=[x^y for x,y in inputs]
        self.assertEqual(and_pred,[0,0,0,1])
        self.assertEqual(xor,[0,1,1,0])
        self.assertEqual(sum(a!=b for a,b in zip(and_pred,xor)),3)

    def test_separate_xor_and_gradient_demonstrations(self):
        h_or=int(1+1-.5>=0)
        h_and=int(1+1-1.5>=0)
        self.assertEqual(int(h_or-2*h_and-.5>=0),0)
        p=1/(1+exp(0))
        self.assertEqual(p,.5)
        gradient=(p-1)*p*(1-p)
        self.assertAlmostEqual(gradient,-.125)
        self.assertAlmostEqual(0-.4*gradient,.05)

if __name__=="__main__":
    unittest.main(verbosity=2)
